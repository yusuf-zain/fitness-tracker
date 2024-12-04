# NUTRIFIT: Nutrition and Fitness
## About Our App
Introducing NUTRIFIT, a groundbreaking 2-in-1 nutrition and fitness application designed specifically for post-operative bariatric surgery patients. As the first of its kind, NUTRIFIT seamlessly integrates  nutrient tracking with fitness tracking to support your journey toward optimal health.

After bariatric surgery, managing nutrient intake becomes crucial due to changes in digestion and reduced food intake capacity. NUTRIFIT offers a tailored solution that helps you meticulously monitor your nutrient consumption, ensuring you meet your dietary needs while avoiding deficiencies. Our intuitive nutrition tracker allows you to log your meals easily, and will provide personalized suggestions based off user data.

But we don't stop at nutrition. Recognizing the importance of physical activity in maintaining weight loss and overall well-being, NUTRIFIT incorporates a fitness module that allows users to track workouts and view progress over time. Whether you're easing back into activity or looking to intensify your workouts, our app provides exercises suitable for your fitness level.

### Key Features:

• Comprehensive Nutrient Tracking: Monitor your intake of calories and macronutrients with ease.

• Fitness Tracking: Access exercise routines tailored to your fitness level and track your progress over time.

• Integrated Progress Charts: Visualize your nutritional intake and fitness achievements through intuitive graphs and charts.

•User-Friendly Interface: Navigate seamlessly between nutrition and fitness modules within a single application.

• Targeted Support: Receive guidance and recommendations specifically designed for post-operative bariatric surgery patients.

### Why Choose NUTRIFIT?

NUTRIFIT stands out by addressing the unique needs of bariatric surgery patients, who often require specialized tools to manage their health effectively. By uniting nutrition and fitness tracking in one app, we eliminate the need to juggle multiple platforms, making it easier for you to stay on top of your health goals. Our dedicated team is committed to providing continuous updates and support to ensure that NUTRIFIT remains an invaluable resource on your journey to wellness.

## Requirements
kivy==2.3.0

kivymd==1.2.0

matplotlib==3.9.2

numpy==2.1.2

pillow==11.0.0

fatsecret==0.4.0

requests==2.32.3

requests-oauthlib==2.0.0

rauth==0.7.3

oauthlib==3.2.2

DateTime==5.5

## Starting The App
Navigate terminal to file location and run:

```python3 main.py```

Ensure all requirements are installed.

## Complications
There were a number of issues which we ran into while creating this app. Early on in the project, I spent 2 days trying to get kivymd working. Turns out pip installed a developer version of the package, causing significant headaches for no reason. Additionally, the kivymd and kivy documentation isn't very robust, creating a huge learning curve for the packages which took me a while to get down. I thought that finding an API to provide the nutrients for all the foods was going to be the hardest part, but it wasn't too much of a hassle.

Another significant problem we ran into was the implementation of the matplotlib graphs into kivy. Kivy has its own personal integration tool called kivy-garden, which has its own matplotlib library. However, I could not get this to work for the life of me. What seemed like an easy process: ```pip install kivy-garden``` followed by ```garden install matplotlib``` ended up sending me on a wild goose chase. For some reason my computer refused to install matplotlib from garden, as garden didn't have permission to install matplotlib. To solve this I went to the file on my computer containing all of the installed packages and I gave the garden tool full permissions -- that didn't work. So then I uninstalled kivy-garden using pip and reinstalled using git. However, my git was out of date, so I updated git and finally installed kivy-garden matplotlib. Alas, I was finally able to get things running. Sike. Kivy-garden matplotlib requires an older version of matplotlib to work with. And so I downgraded my matplotlib, except it didn't work. I tried again and same issue. I then tried dowgrading from pycharm and ran into the same thing. Apparently the version of matplotlib I needed could not run with python 3.12. So now I had reached a dead end. That's when I came up with the ingenious solution to simply upload the pics generated from matplotlib directly to the app interface rather than using the integration and so I did that. The solution makes the app a little laggy, but it was a necessary work around. 

My goal with this app was to solve a real life problem that thousands of patients face. I believe that we achieved that goal with the current project we have.
