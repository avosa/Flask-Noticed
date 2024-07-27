# Flask-Noticed

Flask-Noticed is a Python port of the [Noticed gem for Rails](https://github.com/excid3/noticed), designed for Flask applications. It provides a flexible notification system for your Flask apps, allowing you to manage and deliver notifications through various channels such as database, email, Slack, and more.

## Installation

Flask-Noticed is not yet available on PyPI. You can install it directly from the GitHub repository:

Using Rye:

```bash
rye add --git https://github.com/avosa/flask_noticed.git
```

Using pip:

```bash
pip install git+https://github.com/avosa/flask_noticed.git#egg=flask_noticed
```

Or add the following line to your `requirements.txt` file:

```
git+https://github.com/avosa/flask_noticed.git#egg=flask_noticed
```

## Configuration

Flask-Noticed uses environment variables for configuration. To set these in your project:

1. Create a `.env` file in your project root directory.

2. Add the following variables to your `.env` file:

   ```
   FLASK_ENV=development / production
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///noticed.db
   REDIS_URL=redis://localhost:6379/0
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

3. Adjust the values as needed for your specific setup.

4. In your Flask application, ensure you're loading these environment variables:

   ```python
   from dotenv import load_dotenv
   
   load_dotenv()  # This loads the variables from .env
   
   from flask import Flask
   from flask_noticed import FlaskNoticed
   
   app = Flask(__name__)
   noticed = FlaskNoticed(app)
   ```

Make sure to add `.env` to your `.gitignore` file to avoid committing sensitive information to your repository.

## Quick Start

1. Set up your Flask application:

```python
from flask import Flask
from flask_noticed import FlaskNoticed

app = Flask(__name__)
noticed = FlaskNoticed(app)
```

2. Define a notification:

```python
from flask_noticed import Notification

class CommentNotification(Notification):
    def __init__(self, comment):
        self.comment = comment

    def to_database(self):
        return {
            "type": "new_comment",
            "comment_id": self.comment.id,
            "user_id": self.comment.user_id,
        }

    def to_email(self):
        return {
            "subject": "New comment on your post",
            "body": f"User {self.comment.user.username} commented on your post."
        }
```

3. Send a notification:

```python
@app.route('/comment', methods=['POST'])
def create_comment():
    comment = Comment.create(request.form)
    notification = CommentNotification(comment)
    noticed.notify(comment.post.author, notification)
    return redirect(url_for('post', id=comment.post_id))
```

## Additional Configuration

You can configure additional settings for Flask-Noticed in your Flask app:

```python
app.config['NOTICED_DATABASE_BACKEND'] = 'sqlalchemy'
app.config['NOTICED_EMAIL_BACKEND'] = 'flask_mail'
app.config['NOTICED_SLACK_WEBHOOK'] = 'https://hooks.slack.com/services/...'
```

## Delivery Methods

Flask-Noticed supports various delivery methods:

- Database
- Email
- Slack
- Apple Push Notifications
- Firebase Cloud Messaging
- Custom delivery methods

### Adding a Custom Delivery Method

```python
from flask_noticed import DeliveryMethod

class SMSDeliveryMethod(DeliveryMethod):
    def deliver(self, recipient, notification):
        # Implement SMS sending logic here
        pass

noticed.add_delivery_method('sms', SMSDeliveryMethod)
```

## Retrieving Notifications

```python
@app.route('/notifications')
@login_required
def notifications():
    notifications = noticed.get_notifications(current_user)
    return render_template('notifications.html', notifications=notifications)
```

## Marking Notifications as Read

```python
@app.route('/notifications/mark_read', methods=['POST'])
@login_required
def mark_notifications_read():
    noticed.mark_as_read(current_user, request.form.getlist('notification_ids'))
    return redirect(url_for('notifications'))
```

## Contributing

Contributions to Flask-Noticed are welcome and appreciated! To ensure the quality and reliability of the library, we have the following guidelines:

1. All contributions must include appropriate tests. Pull requests without tests will not be merged.

2. Before submitting a pull request, please ensure that:
   - Your code follows the project's coding style and conventions.
   - All existing tests pass successfully.
   - You have added new tests that cover your changes or additions.
   - Your code is well-documented, including docstrings for new functions and classes.

3. To run the tests, use the following command in the project root directory:
   ```
   rye run pytest
   ```

4. Please provide a clear and detailed description of your changes in your pull request.

5. For significant changes or new features, it's recommended to open an issue for discussion before starting work.

__IMPORTANT:__ This project uses rye's `rye format` for formatting Python code. Please make sure to run `rye format` before submitting pull requests.

We appreciate your efforts to improve Flask-Noticed and look forward to your contributions!

## License

This project is licensed under the MIT License.

## Acknowledgements

Flask-Noticed is a port of the [Noticed gem for Rails](https://github.com/excid3/noticed) by Chris Oliver. We are grateful for the original work and concept.