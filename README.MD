<body>
    <h1>Simple Site API</h1>
    <a href="#"> Link to project </a>
    <p>
        This project is a straightforward API deployed on Render, designed to allow users to manage the content of their websites dynamically. Users can update services, approve or manage reviews, edit bio information, and send emails to clients.
    </p>

    <hr>

    <h2>Key Features</h2>
    <ul>
        <li><strong>Dynamic Content Management:</strong>
            <ul>
                <li>Add or modify services offered.</li>
                <li>Approve and manage customer reviews.</li>
                <li>Edit bio information such as name, description, and contact details.</li>
                <li>Send and receive emails through the API.</li>
            </ul>
        </li>
        <li><strong>Role-Based Access Control:</strong>
            <ul>
                <li>Only authenticated administrators can add, update, or delete services, approve reviews, and modify bio information.</li>
            </ul>
        </li>
    </ul>

    <hr>

    <h2>Technologies & Skills Gained</h2>
    <ul>
        <li><strong>CRUD Functionalities:</strong> Mastered create, read, update, and delete operations.</li>
        <li><strong>Deployment:</strong> Successfully deployed the API using Render.</li>
        <li><strong>MongoDB:</strong> Implemented database storage and management.</li>
        <li><strong>Testing:</strong> Ensured reliability through tools like Postman and Pytest.</li>
        <li><strong>JWT Authentication:</strong> Secured routes with token-based authentication.</li>
        <li><strong>CORS:</strong> Enabled secure communication between frontend and backend.</li>
    </ul>

    <hr>

    <h2>API Endpoints</h2>

    <h3>1. Review Route</h3>
    <p>Manages user reviews with six endpoints:</p>
    <ul>
        <li><strong>Create, Read, Update, and Delete</strong> reviews by the user.</li>
        <li><strong>Admin Privileges:</strong> Admins can review and approve posts before publishing or delete reviews if necessary.</li>
    </ul>

    <h3>2. Service Route</h3>
    <p>Manages services offered with five endpoints:</p>
    <ul>
        <li><strong>Create, Read, Update, and Delete</strong> services, exclusively accessible by the admin.</li>
    </ul>

    <h3>3. Bio Route</h3>
    <p>Manages user bio information with three endpoints:</p>
    <ul>
        <li><strong>Create Bio:</strong> Used during initial setup (only once).</li>
        <li><strong>Read Bio:</strong> Fetch the user’s bio details, including name, email, profile picture, and description.</li>
        <li><strong>Update Bio:</strong> Edit bio information for updates or corrections.</li>
    </ul>

    <h3>4. SendMail Route</h3>
    <p>Provides functionality for email management:</p>
    <ul>
        <li>Receive emails from customers.</li>
        <li>Send emails when logged in as an admin.</li>
    </ul>

    <hr>

    <h2>Security</h2>
    <p>
        All sensitive routes (services, bio, and review approval) are secured with JWT authentication. Only authenticated admins can make changes, ensuring full control and data integrity.
    </p>

    <p>
        This project was an excellent opportunity to practice and enhance backend development skills, focusing on security, scalability, and user management.
    </p>

</body>
