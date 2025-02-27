import datetime
import tempfile
from dataBase import save_file_to_db
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.workout_message import WorkoutMessage
from fit_tool.profile.messages.workout_step_message import WorkoutStepMessage
from fit_tool.profile.profile_type import Sport, Intensity, WorkoutStepDuration, WorkoutStepTarget, Manufacturer, FileType


def workoutBuilder(infoWorkout):
    file_id_message = FileIdMessage()
    file_id_message.type = FileType.WORKOUT
    file_id_message.manufacturer = Manufacturer.DEVELOPMENT.value
    file_id_message.product = 0
    file_id_message.time_created = round(
        datetime.datetime.now().timestamp() * 1000)
    file_id_message.serial_number = 0x12345678
    workout_steps = []
    nSteps = len(infoWorkout.min)
    for i in range(0, nSteps):

        step = WorkoutStepMessage()
        step.workout_step_name = 'Warm up 10min in Heart Rate Zone 1'
        step.intensity = Intensity.WARMUP
        step.duration_type = WorkoutStepDuration.TIME
        step.duration_time = int(infoWorkout.min[i])
        step.target_type = WorkoutStepTarget.HEART_RATE
        step.target_hr_zone = int(infoWorkout.zone[i])
        workout_steps.append(step)

    workout_message = WorkoutMessage()
    workout_message.workoutName = 'Tempo Bike'
    workout_message.sport = Sport.CYCLING
    workout_message.num_valid_steps = len(workout_steps)

    # We set autoDefine to true, so that the builder creates the required
    # Definition Messages for us.
    builder = FitFileBuilder(auto_define=True, min_string_size=50)
    builder.add(file_id_message)
    builder.add(workout_message)
    builder.add_all(workout_steps)

    fit_file = builder.build()

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    fit_file.to_file(temp_file.name)
    Bindata = save_file_to_db(
        infoWorkout.FileName, temp_file.name, infoWorkout.min, infoWorkout.zone)
    return Bindata
