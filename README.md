Sure, here's an updated README file including the new blog system feature:

# Django User Signup and Login Application with Blog System

This Django application allows users to sign up as patients or doctors, log in securely, and access their respective dashboards displaying their profile details. Additionally, it features a blog system where doctors can upload blog posts, and patients can view them.

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

  - Doctors Usernames : [doc1, doc2]
  - Patients username : [pat1, pat2]
  - Common Password : Sriram66#

## Usage

1. **Signup**: Users can sign up as either patients or doctors.
2. **Login**: Secure login functionality is provided.
3. **Blog System**:
   - Doctors can create, view, and manage their blog posts.
   - Patients can view categorized lists of non-draft blog posts.

## Technologies Used

- Django
- Bootstrap
- MySQL (for production)
- AWS (for deployment)

## Contributing

Contributions are welcome! If you have any suggestions or find issues, please open an issue or pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.