pip install -r ceng495hw1/requirements.txt #To build the app requirements are needed. With this line of code they are downloaded.
gunicorn "ceng495hw1:create_app()" #The app is running with this line of code.

https://ceng495hw1-85tl.onrender.com/ #This is the link to webpage.

Admin User Email: e2380301@ceng.metu.edu.tr
Admin User Password:12345678

I used a base.html for this app and deployed the contents by extending that html. All those listings and etc. are the extensions to base.html. It helped me with the non changing all the page and just focusing on the job that is doing and representing.

Users can login or register from the buttons located at the top right corner. After logging in users can see add listing button and logout button at the top right corner.
By clicking those users can logout or instert a listing easily. After logging in user will see last 100 added items. Above them categories will be present. When the user clicks on the category only the items listed on that categories will be listed. If the user clicks on the title of the listing he/she will be directed to that listing's view page where user can see all the attributes of that listing. If and only if the user is logged in can see the phone number of the listing owner.

I chose flask and python for this app because it's easy to use and understand. Since it is not a big data needed app this also made me choose flask.
