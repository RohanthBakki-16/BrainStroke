# Brain Stroke Detection System

A Django-based web application for AI-powered stroke detection from MRI/CT scans using deep learning (U-Net model).

## Features

- User authentication with role-based access (Admin/Doctor)
- Upload and analyze MRI/CT brain scan images
- Mock U-Net style deep learning model for stroke detection
- View diagnosis results with segmented images
- Dashboard with statistics and filtering
- Patient management system

## Project Structure

```
brainstrokediagnosis/
├── stroke_detection_project/  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                  # User authentication app
├── diagnosis/                 # ML and diagnosis app
│   └── ml_model/              # ML prediction module
├── dashboard/                 # Dashboard and stats app
├── templates/                 # HTML templates
├── static/                    # CSS and JS files
├── media/                     # Uploaded images
├── manage.py
└── requirements.txt
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Django>=4.2 Pillow>=10.0 numpy>=1.24
```

### 2. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional - for Admin access)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

Open your browser and navigate to: `http://127.0.0.1:8000/`

## Usage

### 1. Register/Login
- Go to `/register/` to create a new account
- Choose role: Doctor or Admin
- Login at `/login/`

### 2. Upload Scan
- Navigate to "Upload Scan" from the dashboard
- Enter patient details (name, age, gender)
- Select scan type (MRI or CT)
- Upload the brain scan image
- Click "Analyze Scan" to run prediction

### 3. View Results
- View detailed results with original and segmented images
- See stroke detection status, type, and confidence score

### 4. Dashboard
- View statistics: total scans, strokes detected
- Filter by patient or date
- View all patients and their scan history

## URLs

| Path | Description |
|------|-------------|
| `/login/` | User login |
| `/register/` | User registration |
| `/logout/` | User logout |
| `/dashboard/` | Main dashboard |
| `/diagnosis/upload/` | Upload new scan |
| `/diagnosis/result/<id>/` | View result detail |
| `/dashboard/results/` | All results with filters |
| `/dashboard/patients/` | All patients |
| `/dashboard/statistics/` | Statistics page |

## Mock ML Model

The `diagnosis/ml_model/predict.py` contains a mock prediction function that simulates a U-Net model. To integrate a real model:

1. Replace the `predict_stroke()` function with your trained model inference
2. Use TensorFlow/PyTorch to load your trained U-Net weights
3. Update the preprocessing to match your model's input requirements

## Technologies Used

- **Backend**: Django 4.2+
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **ML**: NumPy, Pillow (Mock model for demo)
- **Icons**: Bootstrap Icons

## Security Features

- CSRF protection
- Login required for diagnosis/dashboard
- Role-based access control
- Secure password handling

## License

This project is for educational/demonstration purposes.