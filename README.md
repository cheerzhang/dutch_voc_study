# Dutch Vocabulary Learning Tool

This is a Streamlit application designed to help users learn Dutch vocabulary. The application allows users to search, add, and view Dutch nouns and verbs, along with their English translations, difficulty levels, and more. All data is stored and updated in CSV files hosted on GitHub.

## Features

- ### Search Nouns and Verbs
  Search for Dutch nouns and verbs in the database and view their details, including plural forms, gender, past tense, and more.

- ### Add New Entries
  Add new nouns and verbs to the database with details like plural forms, translations, and difficulty levels.

- ### View All Entries
  View all the nouns and verbs stored in the database.


## How to Access the Application

The application is hosted on Streamlit Cloud. You can access it via the following link:

[**Dutch Vocabulary Learning Tool on Streamlit**](https://dutchvocstudy.streamlit.app/)


## GitHub Integration

The application integrates with GitHub to store and manage CSV data files. The following features are included:

- **Read Data from GitHub**  
  The application reads the latest data from GitHub CSV files using the GitHub Raw URLs.

- **Update Data on GitHub**  
  When new data is added or existing data is modified, the changes are committed back to the GitHub repository.

### Important Notes

- Make sure your GitHub Personal Access Token has the necessary permissions (`repo`).
- Always handle your PAT securely; do not share it publicly or hard-code it in your application.

## Contribution

Feel free to fork the repository and submit pull requests. Please ensure that your contributions follow the project's coding standards and include necessary documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact the repository owner.
