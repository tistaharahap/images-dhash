# Images Dhash

This is a simple demo demonstrating the ease and accuracy of the Dhash algorithm to compare 2 different images and
predict similarities. Sourced form [here](http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html).

Massively inspired from Iconfinder [here](http://blog.iconfinder.com/detecting-duplicate-images-using-python/).

## Short Explanation

Dhash will likely endure image manipulations such as scaling, aspect ratio changes, brightness, contrast and even
changing colors. The steps below taken from the source above will explain why:

1. **Reduce Size**. The fastest way to remove high frequencies and detail is to shrink the image. In this case, shrink it to
9x8 so that there are 72 total pixels. (I'll get to the "why" for the odd 9x8 size in a moment.) By ignoring the size
and aspect ratio, this hash will match any similar picture regardless of how it is stretched.
2. **Reduce Color**. Convert the image to a grayscale picture. This changes the hash from 72 pixels to a total of 72 colors.
(For optimal performance, either reduce color before scaling or perform the scaling and color reduction at the same time.)
3. **Compute the difference**. The dHash algorithm works on the difference between adjacent pixels. This identifies the
relative gradient direction. In this case, the 9 pixels per row yields 8 differences between adjacent pixels. Eight rows
of eight differences becomes 64 bits.
4. **Assign bits**. Each bit is simply set based on whether the left pixel is brighter than the right pixel. The order does
not matter, just as long as you are consistent. (I use a "1" to indicate that P[x] < P[x+1] and set the bits from left
to right, top to bottom using big-endian.)

### Distances Thresholds

- 0 is exact match
- 1 <= distance <= 10 is variance match
- More than 10 is not a match

## Dependencies & Running

```bash
$ git clone git@gitlab.icehousecorp.com:batista/images-dhash.git
$ cd images-dhash
$ CFLAGS=-Wunused-command-line-argument-hard-error-in-future sudo -E pip install -r reqs
$ cd deps/Imaging-1.1.7
$ CFLAGS=-Wunused-command-line-argument-hard-error-in-future sudo -E python setup.py install
$ cd ..
$ python app.py
```

## Endpoints

These are the current endpoints.

### Single Image Hash [POST]
+ Request (multipart/form-data)

```
file:reco_image
```

+ Response (application/json)

```
{
    "code": 200,
    "message": "ok",
    "payload": {
        "dhash": "f3b32737973b556d"
    }
}
```

### Compare 2 Different Images [POST]
+ Request (multipart/form-data)

```
file:reco_image
```

+ Response (application/json)

```
{
  "status": 200,
  "message": "ok",
  "payload": {
    "prediction": {
      "distance": 2,
      "prediction": "Variance Match"
    },
    "dhashes": {
      "reco_image2": "f3b32737973b556d",
      "reco_image1": "f3b327379f33556d"
    }
  }
}
```
