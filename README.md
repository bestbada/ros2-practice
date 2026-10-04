# ROS2 Practice

ROS 2 Humble의 핵심 통신 방식과 도구를 직접 작성하고 실행하며 익힌 실습 저장소입니다.  
turtlesim을 대상으로 토픽·서비스·액션·파라미터를 다루고, launch 구성과 URDF 로봇 모델 시각화까지 실습했습니다.

## 📂 구성

이 저장소는 실습 주제별로 **독립된 워크스페이스 4개**로 나뉘어 있습니다. 각각 따로 빌드합니다.

| 워크스페이스 | 패키지 | 실습 내용 |
|---|---|---|
| `dev_ws/ros` | `my_first_package`, `my_first_package_msgs` | 토픽 발행·구독, 커스텀 msg·srv·action 정의, 서비스 서버, 액션 서버, 파라미터 |
| `launch_ws` | `launch_py`, `substitutions_py` | Python launch 파일, launch 인자와 substitution, 이벤트 핸들러 |
| `move_urdf` | `urdf_r2d2` | URDF 모델과 `robot_state_publisher`로 움직이는 로봇 TF 발행 |
| `my_urdf` | `my_urdf` | URDF 기본 구조 작성과 RViz 표시 |

### my_first_package 노드

| 실행 이름 | 통신 방식 | 동작 |
|---|---|---|
| `my_publisher` | 토픽 발행 | `/turtle1/cmd_vel`로 속도 명령을 0.5초마다 발행해 거북이를 원 운동시킴 |
| `my_subscriber` | 토픽 구독 | `/turtle1/pose`를 구독해 위치 출력 |
| `turtle_cmd_and_pose` | 구독 + 커스텀 msg 발행 | 속도 명령과 현재 위치를 묶어 `CmdAndPoseVel` 메시지로 `/cmd_and_pose`에 발행 |
| `my_service_server` | 서비스 서버 | `MultiSpawn` 요청 개수만큼 거북이를 원형으로 배치해 생성 |
| `dist_turtle_action_server` | 액션 서버 + 파라미터 | 목표 이동 거리까지 거북이를 움직이며 남은 거리를 피드백으로 전송 |

## ⚙️ 환경

- ROS 2 Humble
- 필요한 추가 패키지: `turtlesim`, `demo_nodes_cpp`, `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`

## 🚀 빌드와 실행

### dev_ws: 토픽·서비스·액션

```bash
cd dev_ws/ros
colcon build
source install/setup.bash

# 터미널 1
ros2 run turtlesim turtlesim_node

# 터미널 2 (각 실습마다 하나씩)
ros2 run my_first_package my_publisher
ros2 run my_first_package my_service_server
ros2 run my_first_package dist_turtle_action_server
```

서비스와 액션 호출 예시:

```bash
ros2 service call /multi_spawn my_first_package_msgs/srv/MultiSpawn "{num: 5}"
ros2 action send_goal /dist_turtle my_first_package_msgs/action/DistTurtle \
  "{linear_x: 1.0, angular_z: 0.0, dist: 2.0}" --feedback
```

### launch_ws: launch 실습

```bash
cd launch_ws
colcon build
source install/setup.bash
ros2 launch launch_py my_script_launch.py
ros2 launch substitutions_py main_launch.py
```

### move_urdf / my_urdf: URDF 시각화

```bash
cd move_urdf
colcon build
source install/setup.bash
ros2 launch urdf_r2d2 demo_launch.py
# 다른 터미널에서 rviz2 실행 후 Fixed Frame을 odom으로 설정
```

```bash
cd my_urdf
colcon build
source install/setup.bash
ros2 launch my_urdf simple_display.launch.py
```

## 📚 참고 자료와 라이선스

| 워크스페이스 | 참고 자료 | 라이선스 |
|---|---|---|
| `dev_ws/ros` | 핑크랩(PinkLab) ROS 2 강의 실습 | 강의 자료 기반으로, 별도의 공개 라이선스를 부여하지 않습니다 |
| `launch_ws`, `move_urdf` | [ROS 2 공식 문서](https://docs.ros.org/en/humble/) Launch, URDF 튜토리얼 | 원 문서의 CC BY 4.0을 따릅니다 |
| `my_urdf` | [ros/urdf_tutorial](https://github.com/ros/urdf_tutorial) | 원 저장소의 BSD 3-Clause를 따릅니다 |

이 저장소는 학습 기록용이며, 각 실습의 원저작권은 위 자료의 작성자에게 있습니다.

## 🛠️ 직접 수정한 내용

`dist_turtle_action_server`에서 아래 문제를 찾아 고쳤습니다.

- 이동 거리 계산 함수의 들여쓰기 오류로, 두 번째 호출부터 변수가 정의되지 않아 액션이 중단되던 문제
- 액션 결과 필드 이름이 `.action` 정의(`pose_x`, `pose_y`)와 달라 결과 전송에서 오류가 나던 문제
- 파라미터 이름 오타(`quantile)time`)로 `quantile_time` 변경이 반영되지 않던 문제
