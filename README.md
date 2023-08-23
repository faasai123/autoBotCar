# autoBotCar
The car's motion is facilitated by its four wheels. The front two wheels are driven by a Lego Spike Prime Motor, while the rear two wheels follow the turning pattern. The turning radius is relatively tight, and the wheels on the opposite side of the intended turn direction are engaged. The chosen motor, the Lego Spike Prime Motor, is connected to the Raspberry Pi Build Hat in the 2-wheel drive (2WD) configuration at the front of the car. The decision to use Lego components stems from the desire to position the motor on the lower section of the car, allowing for the placement of other components such as the downward-tilted camera body at the front. This arrangement ensures clear visibility of traffic lights. The car is equipped with an rplidar A1 M6 sensor at the front, working in tandem with the Raspberry Pi 4 and Raspberry Pi Build Hat atop the Lego chassis. These components collaborate to accurately gauge distances from curbs and traffic lights, enhancing the car's navigational abilities. Power is supplied by a rechargeable 12V 10A battery, which is then converted to 8V 6A using a converter. Additionally, a conveniently located switch at the rear of the car facilitates easy power control. The car's design prioritizes a centered center of gravity, achieved by positioning the relatively heavy battery at the center. This strategic design choice prevents wheel spillage during movement.

The system's power supply is provided by a 12V 10A battery, exceeding the maximum power intake capacity of the Raspberry Pi Build Hat. To ensure compatibility, a converter is employed, effectively adjusting the power output to a more manageable 8V 6A. This modification aligns with the precise power demands of the Raspberry Pi 4, safeguarding its optimal functioning and longevity.

Central to the system's operation is the HuskyLens camera, a pivotal sensor responsible for capturing and analyzing mission-critical data. Collaborating seamlessly with the RPLIDAR A1 M6, this synergy forms the foundation for sophisticated operations. Through this integration, a dynamic system of color-based directional control is achieved. The cooperative efforts of these components culminate in the system's ability to make informed decisions about its course of action.

The RPLIDAR A1 M6 takes on the crucial task of real-time obstacle detection. By accurately gauging the distances between the vehicle and its immediate surroundings, encompassing field walls and traffic light poles, it ensures a comprehensive understanding of the operational environment. This capacity serves a dual purpose: firstly, it acts as a preventive measure against potential collisions, and secondly, it plays a pivotal role in calculating the most efficient and safe turning trajectories, taking into account the distance from the nearest traffic light pole.

To achieve effective integration, the HuskyLens camera is intricately connected to the Raspberry Pi 4. This connection is established through a series of specific color-coded cables: the red cable is meticulously linked to VCC to ensure proper power supply, the green cable is dedicated to SDA for robust data transmission, the blue cable is committed to SCL to facilitate seamless communication, and the black cable is securely fastened to GND, completing the essential grounding connection. This meticulous configuration guarantees the camera's seamless interaction with the Raspberry Pi 4, enabling it to contribute actively to the system's overall functionality and mission success.

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

The procedure for generating, compiling, and transferring code to the controller involves several steps. Initially, the Ubuntu operating system is employed on the Raspberry Pi 4. The Build Hat is then connected, and the Build Hat library is installed. Subsequently, the code is authored in Python 3 using Visual Studio Code, establishing a connection via WiFi through the Remote - SSH extension.
