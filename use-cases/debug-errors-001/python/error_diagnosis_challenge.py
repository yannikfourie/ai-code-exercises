#======================================================================
#Error diagnosis challenge
#Exercise:Tracing Error Message and stack traces
#Error scenario: MemoryError in image_processing.py
#======================================================================


#======================================================================
#Section 1: Original Buggy Code 
#=======================================================================

#image_processing.py (original buggy code)
#----------------------------------------------------------------------
#import numpy as np
#from PIL import Image
#import os
#
#def process_image(image_path):
#     img = Image.open(image_path)
#     # BUG 1: Array is 5000x5000x64 of float64 = ~14.9 GB per image
#     # BUG 2: img is opened but never actually used
#     image_data = [[[float(x) for x in range(64)] for _ in range(5000)] for _ in range(5000)]
#     return np.array(image_data)
#
# def process_images(image_files):
#     all_image_data = []
#     for image_file in image_files:
#         # BUG 3: Every image array is kept in memory simultaneously - never released
#         all_image_data.append(load_and_process(image_file))
#     return all_image_data
#
# def main():
#     image_directory = "sample_images"
#     image_files = [os.path.join(image_directory, f)
#                    for f in os.listdir(image_directory) if f.endswith('.jpg')]
#     processed_data = process_images(image_files)
#     print(f"Processed {len(processed_data)} images")
#
# if __name__ == "__main__":
#     main()


# =============================================================================
# SECTION 2: STACK TRACE
# =============================================================================

# Traceback (most recent call last):
#   File "image_processor.py", line 28, in <module>
#     main()
#   File "image_processor.py", line 23, in main
#     processed_data = process_images(image_files)
#   File "image_processor.py", line 14, in process_images
#     all_image_data.append(load_and_process(image_file))
#   File "image_processor.py", line 9, in load_and_process
#     image_data = [[[float(x) for x in range(64)] for _ in range(5000)] for _ in range(5000)]
# MemoryError


# =============================================================================
# SECTION 3: ERROR DESCRIPTION AND WHAT IT MEANS
# =============================================================================

# What is a MemoryError?
# -----------------------
# A MemoryError means Python tried to allocate a block of RAM and the operating
# system refused - there simply wasn't enough free memory to fulfil the request.
#
# In plain terms:
#   Think of your computer's RAM like a physical desk. Your program is trying to
#   spread out 150+ enormous spreadsheets across it all at once. The desk is full
#   and there is no room left to place anything new - so Python stops immediately.
#
# Key characteristics of this error:
#   - The program halts completely with no recovery
#   - The error message itself contains NO line number - just "MemoryError"
#   - You must read the stack trace carefully to find where allocation happened
#   - It does NOT mean your logic is wrong - it means your resource usage is wrong
#
# Memory calculation for this specific crash:
#   5000 rows x 5000 columns x 64 channels x 8 bytes (float64) = 16,000,000,000 bytes
#                                                               = ~14.9 GB PER IMAGE


# =============================================================================
# SECTION 4: ROOT CAUSE IDENTIFICATION
# =============================================================================

# There are THREE compounding root causes - each one makes the situation worse:
#
# ROOT CAUSE 1 - The array is completely detached from the actual image (Line 7 vs Line 9)
# -----------------------------------------------------------------------------------------
# img = Image.open(image_path)   <-- real image is loaded here...
# image_data = [[[float(x) ...   <-- ...but img is NEVER used again
#
# The massive array is 100% synthetic. It is built from hardcoded numbers that
# have no connection to the image that was opened. The program is accidentally
# doing two separate things when it should only be doing one.
#
#
# ROOT CAUSE 2 - Hardcoded dimensions are unrealistically enormous (Line 9)
# -------------------------------------------------------------------------
# range(5000) x range(5000) x range(64)
#
# No standard photograph requires a 5000x5000x64 array. These numbers were never
# derived from the input - they are magic numbers that happen to cause a ~15 GB
# allocation every single time the function runs, regardless of the actual image size.
#
#
# ROOT CAUSE 3 - All processed images are held in memory simultaneously (Line 14)
# --------------------------------------------------------------------------------
# all_image_data.append(load_and_process(image_file))
#
# append() keeps EVERY array alive in the list for the entire program duration.
# With 10 images in the directory:  10 x ~15 GB = ~150 GB held at once
# None of it is released until process_images() returns - which it never does.


# =============================================================================
# SECTION 5: SUGGESTED SOLUTION
# =============================================================================

# Three targeted fixes - one per root cause:
#
# FIX 1: Use the actual image data instead of a synthetic array
#   BEFORE: image_data = [[[float(x) for x in range(64)] for _ in range(5000)] for _ in range(5000)]
#   AFTER:  image_data = np.array(img, dtype=np.uint8)
#
#   The img object already contains the pixel data. Converting it directly means
#   the array size is always proportional to the real image, not a hardcoded constant.
#
#
# FIX 2: Use the correct data type (uint8 instead of float64)
#   BEFORE: float(x)   --> float64 = 8 bytes per value
#   AFTER:  dtype=np.uint8           --> uint8  = 1 byte per value  (8x smaller)
#
#   Pixel values are integers 0-255. uint8 is the natural fit. Only convert to
#   float32/float64 if you specifically need to perform mathematical operations.
#
#
# FIX 3: Process one image at a time using a generator
#   BEFORE:
#       def process_images(image_files):
#           all_image_data = []
#           for image_file in image_files:
#               all_image_data.append(load_and_process(image_file))  # accumulates forever
#           return all_image_data
#
#   AFTER:
#       def process_images(image_files):
#           for image_file in image_files:
#               yield load_and_process(image_file)  # hands off one, frees it, loads next
#
#   A generator means peak memory = size of ONE image, regardless of directory size.


# =============================================================================
# SECTION 6: LEARNING POINTS
# =============================================================================

# LEARNING POINT 1 - Verify that loaded resources are actually used
# -----------------------------------------------------------------
# Opening a file and then ignoring it is an easy mistake, especially when code
# is written incrementally. Any variable assigned near the top of a function and
# never referenced again is a warning sign worth investigating before running the code.
#
#
# LEARNING POINT 2 - Calculate memory cost BEFORE writing allocation code
# -----------------------------------------------------------------------
# A quick mental calculation catches problems at design time, not runtime:
#
#   Memory (bytes) = dimension1 x dimension2 x channels x bytes_per_value
#
#   float64 = 8 bytes  |  float32 = 4 bytes  |  uint8 = 1 byte
#
# If the result is in the gigabytes, reconsider the approach before writing a line.
#
#
# LEARNING POINT 3 - Match data types to the actual data they represent
# ---------------------------------------------------------------------
# Python's built-in float() and NumPy's default float64 are convenient defaults
# but not always appropriate. Choosing a dtype should be deliberate:
#
#   - Storing pixel values       --> uint8
#   - Neural network input/math  --> float32
#   - Scientific precision       --> float64 (only when genuinely required)
#
#
# =============================================================================
# SECTION 7: REFLECTION QUESTIONS
# =============================================================================

# 1: How did the AI's explanation compare to documentation found online?
# -----------------------------------------------------------------------
# The official Python docs describe MemoryError as simply "raised when an
# operation runs out of memory" - accurate but not actionable. The AI explanation
# went further by identifying the three specific compounding causes, calculating
# the exact memory footprint (14.9 GB), and tracing the disconnect between the
# opened image variable and the synthetic array none of which any error message
# or documentation page would surface on its own.
#
#
# 2: What aspects would have been difficult to diagnose manually?
# ---------------------------------------------------------------
# The most deceptive part is that img = Image.open(image_path) succeeds without
# error. A developer could spend significant time checking file paths, Pillow
# installation, or image format compatibility when the real problem is three
# lines later in completely unrelated code. The bug hides behind a working operation.
#
#
# 3: How would you modify your code to provide better error messages in the future?
# ---------------------------------------------------------------------------------
# Add a memory size check before allocation so the program fails with a clear
# explanation rather than a bare MemoryError:
#
#   def load_and_process(image_path):
#       img = Image.open(image_path)
#       w, h = img.size
#       estimated_mb = (h * w * 3 * 8) / (1024 ** 2)   # float64 worst case
#       print(f"[DEBUG] {image_path} -> {w}x{h}, ~{estimated_mb:.1f} MB")
#       if estimated_mb > 500:
#           raise ValueError(f"Image too large to process safely: {estimated_mb:.0f} MB")
#       return np.array(img, dtype=np.uint8)
#
#
# 4: Did the AI help understand not just the fix, but the underlying concepts?
# -----------------------------------------------------------------------------
# Yes three underlying concepts became clear through this exercise:
#
#   dtype selection    - the difference between uint8, float32, and float64 and
#                        when each is appropriate for image data
#
#   generator vs list  - why yield is fundamentally better than .append() for
#                        large sequential data processing and how memory is freed
#
#   memory arithmetic  - how to estimate RAM usage before writing code, treating
#                        it as a design habit rather than an afterthought
