# autoBotCar
This report focuses on an advanced self-driving car system, which involves the use of technology to enable a car to move on its own and make decisions. The car's movement is made possible by its four wheels, and it is equipped with various components that allow it to navigate, avoid obstacles, and follow traffic rules. In this report, we will explore how this self-driving car system works and the different elements that contribute to its functionality.

The car's four wheels play a crucial role in its movement. The two front wheels are connected to a special motor called the Lego Spike Prime Motor. This motor makes the front wheels turn and move the car forward. The two rear wheels are designed to follow the direction set by the front wheels when the car needs to turn. This coordinated movement helps the car navigate and change its direction smoothly.

The car can make turns with a relatively small turning radius, which means it can make tight turns even in narrow spaces. When the car needs to turn, the wheels on the opposite side of the intended direction of the turn are activated. For example, if the car wants to turn right, the left wheels will be engaged more, making the car turn efficiently. This feature is controlled by a special motor called the Lego Spike Prime Motor, which is connected to a computer called the Raspberry Pi Build Hat. This connection allows the car to be controlled and guided.

Lego components are used in this car system for a specific reason. The Lego Spike Prime Motor is placed in the front part of the car, close to the ground. This placement allows other parts, like a camera, to be placed at the front of the car, facing downward. This design choice is important because it helps the car "see" traffic lights clearly. By using Lego pieces, the car's components are arranged in a way that ensures the camera can detect traffic lights effectively.

The car is equipped with special sensors that help it gather important information about its surroundings. One of these sensors is the rplidar A1 M6, which is positioned at the front of the car. This sensor measures distances between the car and objects like walls or traffic light poles. It uses this information to understand where things are and avoid crashing into them. Another crucial sensor is the HuskyLens camera, which can "see" colors. This camera works together with the rplidar sensor to help the car make smart decisions based on what it "sees."

To make the car work, it needs power. The main source of power is a rechargeable battery with a voltage of 12V and a capacity of 10A. However, the computer, Raspberry Pi Build Hat, can only handle a certain amount of power. To make sure the car gets the right amount of power, a special device called a converter is used. This converter adjusts the power from the battery to a level that the computer can handle, which is 8V and 6A. This ensures that the computer works properly and doesn't get damaged.

The HuskyLens camera is a vital part of the car's ability to "see" and understand the world around it. This camera works in harmony with the rplidar A1 M6 sensor. Together, they allow the car to do things like follow traffic rules based on the colors of traffic lights. For example, when the camera "sees" a red light, the car knows to stay in the right lane. When it "sees" a green light, the car knows to stay in the left lane. This collaboration between the camera and sensor guides the car's actions and helps it make informed choices.

The rplidar A1 M6 sensor is also responsible for detecting obstacles in real time. It measures the distances between the car and things around it, like walls or traffic light poles. This information helps the car understand its environment better. The sensor does two important things: it prevents the car from crashing into things, and it calculates the best way to turn or move around obstacles. It even considers the distance from the nearest traffic light pole to decide on the safest way to go.

The car is programmed to complete specific tasks, or missions. In the first mission, the car needs to avoid hitting walls. It uses the rplidar sensor to measure how far the walls are from the car at different angles. Depending on the measurements, the car chooses one of two strategies:

Moving Straight: The car keeps going forward and uses the rplidar sensor to make sure it doesn't hit the walls on either side.

Turning: If the car detects a wall in front of it, it decides which way to turn based on which wall is closer. For example, if the left wall is closer, the car turns right.

After completing a certain number of turns, the car moves forward to see how close it is to the front pillars and then parks within a designated area.

The second mission involves responding to traffic lights. In addition to using the rplidar sensor, the car also uses the HuskyLens camera to detect the colors of traffic lights. When the camera "sees" a red light, the car knows to stay on the right side. When it "sees" a green light, the car knows to stay on the left side. The car completes a set number of turns and encounters a special road sign. Depending on the color of the sign, it chooses its next action:

Green Sign: The car continues forward in its lane.
Red Sign: The car goes around the obstacle and moves in the opposite direction to avoid it.
Finally, after a few more turns, the car stops after passing the last traffic light pole, making sure it stays within the lane boundaries.

To make all of this work, the car needs the right instructions. These instructions are called code. The process begins by using a computer system called Ubuntu on the Raspberry Pi 4. The Raspberry Pi Build Hat is connected to the computer, and a special library for it is installed. The code that controls the car's actions is written in a programming language called Python 3. A tool called Visual Studio Code helps write the code, and the connection to the car is established through WiFi using an extension called Remote - SSH.

In conclusion, the advanced self-driving car system is a combination of technology, sensors, and smart programming. It allows the car to move, make decisions, and respond to its surroundings. Through careful design, collaboration between sensors, and intelligent programming, the car can navigate around obstacles, follow traffic rules, and complete missions. This technology represents a significant step forward in the field of autonomous vehicles and offers a glimpse into the exciting possibilities of the future.
