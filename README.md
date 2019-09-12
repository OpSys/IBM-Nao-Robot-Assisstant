# IBM-Nao-Robot-Assisstant

We developed an assistant bot using the Nao bot. The bot's purpose is to help people find what they're looking for in places like the book store, offices, resturants etc. We implement this on the Nao robot. In this code, we use simulators (Choregraphe and V-Rep) to control the robot. We also use Watson services (Speech to text &amp; Text to Speech) for the robot's interaction with humans.

This is a basic implementation. In this code, our robot is a book store assistant that directs  people to a shelf containing the category that the user wants. The book store has three shelves, Comics, Romance and Thriller. When the user asks for one of the categories, the robot will point to the section and shelf containing the requested category. The robot will also offer to walk the human to the shelf.

We were able to get the robot to walk, sit down, stand up, lie on its back or front. You can use those functions as you please and also add other actions as well, which is done in the NaoRobot.py file.  

Possible extentions would be to:  
1. Implement the Watson assistant service for better interaction between the robot and the human - use Natural Language Processing to understand the human. 
2. Use face recognition to identify common people in the place (employees, loyal customers ets.)  
3. Other cool stuff.  

enjoy!
