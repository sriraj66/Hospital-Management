# Django User Signup and Login Application with Blog System and Appointment Booking

This Django application allows users to sign up as patients or doctors, log in securely, and access their respective dashboards displaying their profile details. Additionally, it features a blog system where doctors can upload blog posts, and patients can view them. The application also includes an appointment booking system where patients can book appointments with doctors.

## Features

- **Signup**: Users can register as either patients or doctors with their profile details.
- **Login**: Secure authentication using Django's built-in system.
- **User-Specific Dashboards**: Patients and doctors are redirected to their respective dashboards upon login.
- **Blog System**:
  - Doctors can create new blog posts with the following fields: Title, Image, Category, Summary, Content.
  - Doctors can mark blog posts as drafts.
  - Doctors can view the posts they have uploaded.
  - Patients can view a list of all non-draft blog posts, categorized.
  - Each blog post in the list includes the title, image, and a truncated summary (15 words limit).
- **Appointment Booking System**:
  - Patients can view a list of all doctors in the system.
  - Each list item includes the doctor's profile picture, name, and a "Book Appointment" button.
  - Patients can book an appointment by filling out a form with the required specialty, date, and start time of the appointment.
  - Each appointment is 45 minutes long.
  - Upon confirmation, a calendar event is created for the doctor using Google’s Calendar API.
  - Patients can view the appointment details including the doctor’s name, appointment date, start time, and end time (calculated by the application).

## Blog Categories

The blog system includes the following categories:
- Mental Health
- Heart Disease
- Covid19
- Immunization

## Deployment

This application is deployed at [http://18.118.9.110:8080/](http://18.118.9.110:8080/).

### Access Credentials

- **Admin Panel**: [http://18.118.9.110:8080/admin/](http://18.118.9.110:8080/admin/)
  - Username: admin
  - Password: admin

  - Doctors Usernames: [doc1, doc2]
  - Patients Usernames: [pat1, pat2]
  - Common Password: Sriram66#

## Usage

1. **Signup**: Users can sign up as either patients or doctors.
2. **Login**: Secure login functionality is provided.
3. **Blog System**:
   - Doctors can create, view, and manage their blog posts.
   - Patients can view categorized lists of non-draft blog posts.
4. **Appointment Booking System**:
   - Patients can view a list of all doctors and book appointments.
   - Patients fill out a form to book appointments with details such as required specialty, date, and start time.
   - Appointments are 45 minutes long and create calendar events for doctors using Google’s Calendar API.
   - Patients can view appointment details after confirmation.

## Technologies Used

- Django
- Bootstrap
- MySQL (for production)
- AWS (for deployment)
- Google Calendar API

## Contributing

Contributions are welcome! If you have any suggestions or find issues, please open an issue or pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
