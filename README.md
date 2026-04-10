# Petface

Petface is a web platform that helps owners find their lost cats using facial recognition. Users submit a photo of their cat, and the system matches it against a database of registered cat profiles.

## How It Works

The recognition pipeline runs entirely without neural networks, relying instead on classical computer vision techniques — making it lightweight and practical even with a small dataset.

1. **Face Detection** — uses a pretrained LBP cascade classifier to locate the cat's face in the image.
2. **Landmark Detection** — dlib's shape predictor finds key facial landmarks.
3. **Image Alignment** — the face is transformed so landmarks align to a standard template, normalizing pose across images.
4. **LBP Histogram Encoding** — a Local Binary Pattern Histogram (LBPH) is computed as the face's feature vector.
5. **Classification** — the face is matched to the closest class by LBPH correlation.
6. **Similarity Check** — a t-test compares the new face's similarity to the matched class against intra-class similarities. Returns the cat's ID, `-1` (face found, no match), or `-2` (no face detected).

## Project Structure

```
├── server.py               # Flask API server
├── catfd/                  # Cat face detection module
│   ├── catfd.py            # Detection logic
│   ├── detector.svm        # Trained SVM detector
│   └── predictor.dat       # Dlib landmark predictor
├── db/                     # Cat profile database
│   └── utils.py            # DB helper functions
├── classes/                # Trained recognizer and class data
│   ├── *.cim               # Pickled face images per class
│   └── *.csm               # Pickled intra-class similarity scores
├── website/                # Frontend static files
└── images/                 # Sample/test images
```

## Prerequisites

- Python 3.6+
- OpenCV
- dlib
- Flask + flask-cors
- NumPy

Install dependencies:

```bash
pip install opencv-python dlib flask flask-cors numpy
```

## Running the Server

```bash
python server.py
```

The server starts on `http://0.0.0.0:8080` and serves the frontend from the `website/` folder.

## API Endpoints

### `POST /cat_recognition_api/v1/actions/get_response`

Checks a submitted image against the database.

Request body:
```json
{ "image": "<base64-encoded image>" }
```

Response:
```json
{ "response": "<cat profile object | 'Face detected but no match found' | 'No face detected'>" }
```

### `POST /cat_recognition_api/v1/actions/add_new_profile`

Registers a new cat profile with an image.

Request body:
```json
{
  "image": "<base64-encoded image>",
  "name": "...",
  "owner": "..."
}
```

Response:
```json
{ "response": "<created profile>" }
```

## Core Functions

| Function | Description |
|---|---|
| `CheckImage(img)` | Main entry point. Returns cat ID, `-1` (no match), or `-2` (no face). |
| `TrainFaceRecognizer(folder)` | Retrains the recognizer. Pass a folder of class subfolders to initialize, or `None` to retrain from existing `.cim` files. |
| `ExtractFace(img)` | Detects, aligns, and returns the face region. |
| `RecognizeFace(face)` | Returns the label of the closest matching class. |
| `CheckSimilarity(face, faces, classSimilarities)` | t-test to decide if a face belongs to a class. |
| `AddClass(images, label)` | Creates `.cim` and `.csm` files for a new class. |
| `ModifyClass(img, label)` | Adds a new image to an existing class. |
| `FaceDetectionLBP(img)` | Returns bounding box of detected face. |
| `GetLandmarks(img, face)` | Returns landmark coordinates for a face region. |
| `InnerSimilarity(faces)` | Computes pairwise LBPH correlation within a set of faces. |
| `CalculateSimilarities(face, faces)` | Computes similarity between one face and a set. |

## Data Files

- `*.cim` — pickled lists of face images per class
- `*.csm` — pickled lists of intra-class pairwise similarity scores
- `predictor.dat` — dlib landmark predictor model
- `*.xml` — pretrained cascade classifiers for cat face detection
