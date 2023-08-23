# autoBotCar
The car's motion is facilitated by its four wheels. The front two wheels are driven by a Lego Spike Prime Motor, while the rear two wheels follow the turning pattern. The turning radius is relatively tight, and the wheels on the opposite side of the intended turn direction are engaged. The chosen motor, the Lego Spike Prime Motor, is connected to the Raspberry Pi Build Hat in the 2-wheel drive (2WD) configuration at the front of the car. The decision to use Lego components stems from the desire to position the motor on the lower section of the car, allowing for the placement of other components such as the downward-tilted camera body at the front. This arrangement ensures clear visibility of traffic lights. The car is equipped with an rplidar A1 M6 sensor at the front, working in tandem with the Raspberry Pi 4 and Raspberry Pi Build Hat atop the Lego chassis. These components collaborate to accurately gauge distances from curbs and traffic lights, enhancing the car's navigational abilities. Power is supplied by a rechargeable 12V 10A battery, which is then converted to 8V 6A using a converter. Additionally, a conveniently located switch at the rear of the car facilitates easy power control. The car's design prioritizes a centered center of gravity, achieved by positioning the relatively heavy battery at the center. This strategic design choice prevents wheel spillage during movement.

The power source for the system is a 12V 10A battery, which exceeds the power intake capacity of the Raspberry Pi Build Hat. Thus, a converter is employed to adjust the power output to 8V 6A, aligning with the Raspberry Pi 4's requirements. The key sensor employed to gather mission-critical data is the HuskyLens camera, working in conjunction with the RPLIDAR A1 M6. This collaboration enables color-based directional control. The RPLIDAR assumes the role of identifying the distances between the vehicle and surrounding obstacles, including the field walls and traffic light poles. This functionality safeguards the car against collisions and aids in determining the optimal turning dynamics based on the distance from the traffic light pole. As for the camera's integration, it is linked to the Raspberry Pi 4 using specific color-coded connections: the red cable to VCC, the green cable to SDA, the blue cable to SCL, and the black cable to GND.

In the initial mission, the primary obstacle to address is the wall. To achieve this, a specific strategy is employed, involving the programmed utilization of the RPLIDAR sensor to measure the distances between the car and the wall at various angles. For the right wall, the range is set at 0-68 degrees; for the front wall, it is 69-114 degrees, and for the left wall, it is 115-180 degrees. To navigate without colliding with the wall, two strategies are employed:

Straight Movement: While the car moves straight ahead, the RPLIDAR detects both side walls, allowing the car to maintain a straight trajectory.

Turning Maneuvers: When the RPLIDAR detects the front wall, it identifies which side wall is closer. If the left wall is closer, a right turn is executed. Conversely, if the right wall is closer, a left turn is initiated. The effectiveness of these turns is also enhanced by RPLIDAR's distance detection.

Upon completing 12 turns, the car advances forward and assesses the distance from the front pillars to park, ensuring it remains within the designated boundaries.

In the mission involving traffic lights, the management of the RPLIDAR sensor remains pivotal, but two additional components are introduced: distance detection between traffic light poles and color detection using the HuskyLens camera. Depending on the color detected:

Red Light: The car stays in the right lane.
Green Light: The car stays in the left lane.
After the car has completed eight angled turns, it reaches a pivotal road sign. By examining the color of the sign, the car determines its next action:

Green Sign: The car proceeds forward, maintaining its lane.
Red Sign: The car makes a detour to circumvent the pole, ensuring its stability, and navigates in the opposite direction.
Upon performing four more angled turns, the car halts after passing the last traffic light pole, ensuring it remains within the lane boundaries.






