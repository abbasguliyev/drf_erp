from django.contrib.auth.models import Permission


def create_user(self, validated_data):
    last_user_id = User.objects.all().values_list('id', flat=True).last()
    username = f"user-{last_user_id+1}"
    user = User.objects.create(
        username=username,
        fullname=validated_data['fullname'],
        phone_number_1=validated_data['phone_number_1'],
        photo_ID=validated_data['photo_ID'],
        salary_style=validated_data['salary_style'],
        contract_type=validated_data['contract_type'],
    )
    user.set_password(validated_data['password'])

    try:
        user.back_photo_of_ID = validated_data['back_photo_of_ID']
    except:
        user.back_photo_of_ID = None
    try:
        user.profile_image = validated_data['profile_image']
    except:
        user.profile_image = None

    try:
        user.driving_license_photo = validated_data['driving_license_photo']
    except:
        user.driving_license_photo = None

    try:
        user.start_date_of_work = validated_data['start_date_of_work']
    except:
        user.start_date_of_work = django.utils.timezone.now()

    try:
        user.dismissal_date = validated_data['dismissal_date']
    except:
        user.dismissal_date = None
    try:
        user.salary = validated_data['salary']
    except:
        user.salary = 0

    try:
        user.department = validated_data['department']
    except:
        user.department = None

    try:
        user.company = validated_data['company']
    except:
        user.company = None

    try:
        user.office = validated_data['office']
    except:
        user.office = None

    try:
        user.section = validated_data['section']
    except:
        user.section = None
    try:
        user.position = validated_data['position']
        permission_for_positions = PermissionForPosition.objects.filter(
            position=user.position)
        if permission_for_positions is not None:
            for vp in permission_for_positions:
                permission_group = vp.permission_group
                user.groups.add(permission_group)
    except:
        user.position = None

    try:
        user.phone_number_2 = validated_data['phone_number_2']
    except:
        user.phone_number_2 = None

    try:
        user.team = validated_data['team']
    except:
        user.team = None

    try:
        user.employee_status = validated_data['employee_status']
    except:
        user.employee_status = None
    try:
        user.supervisor = validated_data['supervisor']
    except:
        user.supervisor = None

    try:
        user.note = validated_data['note']
    except:
        user.note = None

    user_permissions = validated_data['user_permissions']
    for user_permission in user_permissions:
        user.user_permissions.add(user_permission)

    # permission_for_positions = get_object_or_404(PermissionForPosition, )
    groups = validated_data['groups']
    for group in groups:
        user.groups.add(group)

    user.save()
    return user
