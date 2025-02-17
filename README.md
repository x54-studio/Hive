# Hive Frontend

This project is the frontend for the Hive news platform, built with React. It provides a responsive UI for viewing articles, managing user authentication, and interacting with the Hive backend API.

## Project Structure

```plaintext
frontend/
├── Dockerfile                # Docker configuration for the frontend container
├── package.json              # NPM configuration and dependencies
├── tailwind.config.js        # Tailwind CSS configuration
├── public/
│   ├── favicon.ico           # Site favicon
│   ├── index.html            # Main HTML file
│   └── robots.txt            # Robots exclusion rules
├── src/
│   ├── App.js                # Main application component with routing and lazy loading
│   ├── AuthContext.js        # Context API for user authentication
│   ├── ThemeContext.js       # Context for managing light/dark theme toggling
│   ├── components/
│   │   ├── AddArticle.js     # Component for adding new articles
│   │   ├── ArticleList.js    # Component for displaying a list of articles
│   │   ├── Layout.js         # Layout component (now with static background color)
│   │   ├── Navbar.js         # Navigation bar component
│   │   └── ThemeToggle.js    # Button component to toggle light/dark mode
│   ├── pages/
│   │   ├── Home.js           # Homepage displaying articles and welcome message
│   │   ├── Login.js          # Login page
│   │   ├── Profile.js        # User profile page
│   │   └── Register.js       # Registration page
│   ├── styles/
│   │   └── index.css         # Global styles (imports Tailwind CSS)
│   ├── index.js              # Entry point for the React application
│   └── tests.js              # (Optional) Frontend tests configuration
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- **Node.js** (version 16 or higher)
- **NPM** or **Yarn**

### Setup

1. Clone the repository.
2. Navigate to the `frontend/` directory.
3. Install dependencies:
   ```bash
   npm install
   ```
   or if you prefer Yarn:
   ```bash
   yarn install
   ```

### Running the Application

Start the development server:
```bash
npm start
```
This will launch the app at [http://localhost:3000](http://localhost:3000).

### Building for Production

To build the app for production:
```bash
npm run build
```
This will create an optimized production build in the `build/` folder.

### Testing

Run frontend tests with:
```bash
npm test
```

## Styling and Theming

- The app uses Tailwind CSS for styling.
- Dark mode is supported using Tailwind's dark mode classes.  
  Ensure that the theme is toggled using the ThemeContext and that the `<html>` element is appropriately set with the dark mode class.

---
