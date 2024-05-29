# Image enhancement

## Brightness adjustment & CLAHE

```python
im = cv2.imread(im_path)
enhanced_im = adjust_gamma(im, 0.4)
enhanced_im = hist_equalize(im)
```

## Binary distribution

```bash
pyinstaller cli.py --onefile -n enhancing

cp ./dist/enhancing /usr/local/bin/
```
