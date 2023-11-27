# SmartDMS Fast Api Server

To run the server ensure that the python installed is 3.10 or above. After that, install this

```bash
# for Windows
pip install virtualenv

# for MacOS
pip3 install virtualenv
```

Now to create a virtual environment:

```bash
virtualenv env
```

Now to start the virtual environment, use the following command:

```bash
source /absolute-path-of-folder/env/Scripts/activate
```

To install the required dependencies in the virtual environment run:

```bash
# For Windows
pip install -r requirements.txt

# For MacOS
pip3 install -r requirements.txt
```

After installing the dependencies, create a file with name `.env` and add the path of Tesseract_OCR server:

```env
TESSERACT_PATH="<path-of-tesseract-server-in-your-laptop>"
```

After adding the path, start the server fastapi server using this command:

```bash
uvicorn main:app --reload
```

### To know about the api endpoints, [click here](REQUEST.md)
