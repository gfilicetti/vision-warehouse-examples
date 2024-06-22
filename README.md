# Vision Warehouse Examples
A set of example scripts to create corpus, assets and index them, showing the power of Vision Warehouse.

> **Note** We'll be using video sample files from this GCS bucket: `gs://cloud-samples-data/video`

Currently we have a copy of the Vision Warehouse Colab notebook with canonical examples from the VW engineering team. New versions of the notebook can be [found here](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/vision/image_warehouse_sdk.ipynb).

## Python Script

The `vw.py` python script includes code that does everything the Vision Warehouse Colab notebook does. It is a work in progress, but it is called with these parameters:

```bash
python -m vw.vw \
    --corpus corp4 \
    --corpus-desc corp4desc \
    --index index4 \
    --index-endpoint indexendpoint4 \
    --clean-corpus \
    --clean-assets \
    --clean-index
```

## REST Command Examples 

Here are a bunch of curl commands that I used to CRUD objects in Vision Warehouse, these are included just for reference.

### List Corpora

```bash
curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora"
```

### Corpora: `9999819062635862512`

### Delete Corpora

```bash
curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512"
```

### List Indices

```bash
curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/indexes"
```

### List Endpoints

```bash
curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/indexEndpoints"
```

### Indices & Endpoints
#### index-99994720693559361194
#### ie-99990348282986011026

### Undeploy Indices

```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json; charset=utf-8" -d "" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/indexEndpoints/ie-99990348282986011026:undeployIndex"
```

### Delete Indices

```bash
curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/indexes/index-99994720693559361194"
```

### Delete Endpoints

```bash
curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/indexEndpoints/ie-99990348282986011026"
```

### Get Assets

```bash
curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets"
```

### Delete Assets

```bash
curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/12984489999593754347"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/3970743097087166713"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/16928765288310686816"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/1648851723324334653"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/5748534923989624318"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/7346271686977019659"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/9999819062635862863"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/8740071360584866062"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/3370434398267398706"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/3789785871989072236"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/3744755575364304940"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/180550742095623448"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/14746247477085307595"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/4292735299976060330"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/15246787935360415117"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/13969458492738947121"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/17697694327559925822"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/1457746186792912907"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/11264167223874733444"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/7903448043031908681"

curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://warehouse-visionai.googleapis.com/v1/projects/99994013451/locations/us-central1/corpora/9999819062635862512/assets/11594329831432114333"
```