
# Evendy     

This simple app will help you find a companion for any musical event in Germany. You can sign up as a companion seeker or search among the already signed up seekers. 
Send invitations or receive them from others - you can decide for yourself who you will go to the event with.
The application was written based on the Django framework. The Ticketmaster Discovery API was used to retrieve event data.


### Technologies
<ul>
<li>Python 3.11</li>
<li>Django</li>
<li>HTML5, CSS3</li>
<li>Bootstrap 4</li>
<li>Docker, docker-compose</li>
</ul>

### Requirements to setup
<ul>
<li>Docker</li>
<li>Docker Compose</li>
</ul>

### Setup
<ol>
<li>Clone this repo:</li>

```git clone https://github.com/marcho4917/Evendy-project.git```

<li>Go to the directory:</li>

```cd Evendy-project```

<li>Start the application using Docker Compose:</li>

```docker compose up --build```

</ol>

The application will be available at http://localhost:8000.

### App functionalities

<ul>
<li>User registration: The app allows users to register an account, allowing them full access to the app's features.</li>
<li>Event Search: Users can browse the list of available events, search them using the search engine.</li>
<li>Participating in events: Users can join events in which they are interested and for which they are looking for a companion.</li>
<li>Cancellation of invitations: Users can easily manage sent and received invitations in the "My invites" tab.</li>
<li>Updating data: Registered users have the possibility to update their profile information.</li>
</ul>

### Preview views

<img src="evendy_project/views_img/main_page.jpg">Main Page|<img src="evendy_project/views_img/new_notification_main_view.jpg">Login user view
:-------------------------:|:-------------------------:
<img src="evendy_project/views_img/event_with_seekers.jpg">Event view|<img src="evendy_project/views_img/login.jpg">Login
<img src="evendy_project/views_img/logout_view.jpg">Logout|<img src="evendy_project/views_img/register.jpg">Register
<img src="evendy_project/views_img/profile_page.jpg">Profile view|<img src="evendy_project/views_img/user_invites_view.jpg">Invitations
<img src="evendy_project/views_img/notifications_view.jpg">Notifications|<img src="evendy_project/views_img/another_user_profile_view.jpg">Another User