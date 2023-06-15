# Jobby

## Introduction
Jobby is a platform that connects homeowners with service providers. It allows homeowners to easily find and hire service providers for various tasks and services. Service providers can showcase their skills and expertise, and homeowners can browse and book services conveniently through the platform.

- Deployed Site: [Jobby](https://jobby-alx.netlify.app)
- Final Project Blog Article: [<i>Coming soon...</i>]
- Author(s) LinkedIn: [Daniel Olah](https://www.linkedin.com/in/daniel-olah-509a7b190/)

## Installation
To run Jobby locally, follow these steps:

1. Clone the repository: `git clone https://github.com/danny-ell/jobby.git`
2. Navigate to the project directory: `cd jobby`
3. Install the dependencies: `pip install -r requirements.txt`
4. Create and Run db Migrations `python manage.py makemigrations && python manage.py migrate`
5. Load the mock data into the db: `python manage.py load_fixtures`
6. Run the development server: `python manage.py runserver`
7. Access Jobby in your browser at: `http://localhost:8000`

## Usage

### Go to http://localhost:8000/

### 1. Type "Plumber"
![Step 1 screenshot](https://images.tango.us/workflows/49d57c2d-9e6d-4e5e-982b-110b8a65cd77/steps/3179aa60-63f3-49de-91db-804bdce7ba19/0d620b63-137c-4d30-a6b3-9d3257b45f54.png?crop=focalpoint&fit=crop&fp-x=0.2667&fp-y=0.6265&fp-z=1.6229&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&blend-align=bottom&blend-mode=normal&blend-x=0&blend-w=1200&blend64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL21hZGUtd2l0aC10YW5nby13YXRlcm1hcmstdjIucG5n&mark-x=211&mark-y=331&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz02MTYmaD05NiZmaXQ9Y3JvcCZjb3JuZXItcmFkaXVzPTEw)

### 2. Click on All Location
![Step 2 screenshot](https://images.tango.us/workflows/49d57c2d-9e6d-4e5e-982b-110b8a65cd77/steps/e597910a-6c52-4926-a96e-6b39d23eb565/d23175b0-c759-405d-a75d-8efd0cb6716e.png?crop=focalpoint&fit=crop&fp-x=0.6090&fp-y=0.6258&fp-z=1.8453&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&blend-align=bottom&blend-mode=normal&blend-x=0&blend-w=1200&blend64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL21hZGUtd2l0aC10YW5nby13YXRlcm1hcmstdjIucG5n&mark-x=266&mark-y=347&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz02NjkmaD02NSZmaXQ9Y3JvcCZjb3JuZXItcmFkaXVzPTEw)

### 3. Click on Lagos, Nigeria
![Step 3 screenshot](https://images.tango.us/workflows/49d57c2d-9e6d-4e5e-982b-110b8a65cd77/steps/85f80549-8c4c-4565-bc36-3aa13ddb6f92/d2865075-fe53-4c83-8272-7e8222813315.png?crop=focalpoint&fit=crop&fp-x=0.5867&fp-y=0.8569&fp-z=1.7827&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&blend-align=bottom&blend-mode=normal&blend-x=0&blend-w=1200&blend64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL21hZGUtd2l0aC10YW5nby13YXRlcm1hcmstdjIucG5n&mark-x=284&mark-y=525&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz02MzImaD04MSZmaXQ9Y3JvcCZjb3JuZXItcmFkaXVzPTEw)

### 4. Click on Get Started
![Step 4 screenshot](https://images.tango.us/workflows/49d57c2d-9e6d-4e5e-982b-110b8a65cd77/steps/14d1100c-d08f-4ec1-9e51-4daf10739ed2/822b5090-4853-470e-bfd8-0c50a188fdc1.png?crop=focalpoint&fit=crop&fp-x=0.8033&fp-y=0.6265&fp-z=2.6224&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&blend-align=bottom&blend-mode=normal&blend-x=0&blend-w=1200&blend64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL21hZGUtd2l0aC10YW5nby13YXRlcm1hcmstdjIucG5n&mark-x=377&mark-y=299&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz00NDcmaD0xNjImZml0PWNyb3AmY29ybmVyLXJhZGl1cz0xMA%3D%3D)

### 5. Click on Plumbing Services…
![Step 5 screenshot](https://images.tango.us/workflows/49d57c2d-9e6d-4e5e-982b-110b8a65cd77/steps/ed5cfebb-3434-4062-8edf-10bf59a7ba02/b38cc39d-b163-483d-828e-26fc6a4191f9.png?crop=focalpoint&fit=crop&fp-x=0.2095&fp-y=0.5542&fp-z=1.4286&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&blend-align=bottom&blend-mode=normal&blend-x=0&blend-w=1200&blend64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL21hZGUtd2l0aC10YW5nby13YXRlcm1hcmstdjIucG5n&mark-x=16&mark-y=185&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz02ODYmaD0zODkmZml0PWNyb3AmY29ybmVyLXJhZGl1cz0xMA%3D%3D)


## Contributing
We welcome contributions to Jobby! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Create a pull request detailing your changes.

## Related Projects
Jobby has no related projects or dependencies
