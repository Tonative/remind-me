# remind-me
A web automated reminder system that reminds tonative members about their tasks timelines by sending automated reminders for tasks start and completion dates using github actions.


## 🚀 Features

- **Send reminder at the start of a project**: This will be done 2 days ahead of the start date, and the member will be reminded everyday until the day the task start day.
- **Send reminder at the end of a project**: This will be done 2 days ahead of the end date, and the member will be reminded everyday until the day the task end day.
- **Github Comments**: Automated comments on GitHub issues and pull requests to keep team members updated on project timelines and deadlines
- **Github Actions**: Automated workflow that runs daily to check project timelines and send notifications through GitHub comments and email alerts


## 🛠️ Contributing to the Project

We welcome contributions from the community! We follow the Fork & Pull Request workflow for contributions. Here's how you can contribute:

### Step 1: Set Up Your Environment

1. **Fork the Repository**:
   - Visit the main repository at `https://github.com/Tonative/remind-me`
   - Click the "Fork" button in the top right corner to create your own copy

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/Tonative/remind-me.git
   cd research-timeline-reminder
   ```

3. **Add the Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/Tonative/remind-me.git
   ```

### Step 2: Create a Feature Branch

1. **Sync with the Upstream Repository**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a New Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Use a descriptive name for your branch (e.g., `feature/added-comments` or `fix/date-issue`)

### Step 3: Make Your Changes

1. **Implement Your Feature or Fix**:
   - Write clean, well-documented code
   - Include comments where necessary

2. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Add meaningful commit message describing your changes"
   ```
   Write clear, concise commit messages that explain what your changes do

### Step 4: Submit a Pull Request

1. **Push Your Changes to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**:
   - Go to your fork on GitHub
   - Click the "Compare & pull request" button for your branch
   - Provide a clear description of your changes
   - Reference any relevant issues using the # symbol (e.g., "Fixes #42")

3. **Wait for Review**:
   - Project maintainers will review your PR
   - Be responsive to any feedback or requests for changes
   - Make additional commits to your branch if needed

### Step 5: After Your PR is Merged

1. **Sync Your Fork**:
   ```bash
   git checkout main
   git fetch upstream
   git merge upstream/main
   git push origin main
   ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or support, please reach out to the project maintainers:
- GitHub Issues: https://github.com/Tonative/remind-me/issues
