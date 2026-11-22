# Uploads and downloads

- For a file input, use `upload_file(selector, path)` with the authorized
  file's absolute path. Verify the selected file in the UI before submitting.
  For custom controls, find the underlying file input after opening the
  uploader.
- For a browser download, trigger it on the intended tab and check that the
  browser reports completion or the expected file finishes writing. Check
  the filename and location before handing off the file or retrying.
