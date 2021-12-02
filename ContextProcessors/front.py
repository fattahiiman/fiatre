from Setting.models import Setting

def public_operations(request):
    if '/admin' not in request.path and request.user.is_authenticated and request.user.is_watching:
        request.user.is_watching = False
        request.user.save()
    return {}

def static_footer_header_variables(request):
    settings = {}

    if '/admin' not in request.path:
        settings['advertise_title'] = Setting.objects.get_or_create(
            key='advertise_title',
            defaults={'key': 'advertise_title',
                      'value': 'اولین VOD تخصصی هنر در ایران'},
        )[0].value

        settings['logo'] = Setting.objects.get_or_create(
            key='logo',
            defaults={'key': 'logo',
                      'value': '/static/front/img/logo.png'},
        )[0].value

        settings['Enamad_logo'] = Setting.objects.get_or_create(
            key='Enamad_logo',
            defaults={'key': 'Enamad_logo',
                      'value': '/static/front/logo2.aspx'},
        )[0].value

        settings['copyright'] = Setting.objects.get_or_create(
            key='copyright',
            defaults={'key': 'copyright',
                      'value': 'Copyright © 2020 - 2021 Fiatre. All Rights Reserved'},
        )[0].value

        settings['telegram'] = Setting.objects.get_or_create(
            key='telegram',
            defaults={'key': 'telegram',
                      'value': 'Fiater'},
        )[0].value

        settings['watsapp'] = Setting.objects.get_or_create(
            key='watsapp',
            defaults={'key': 'watsapp',
                      'value': '989021616483'},
        )[0].value

        settings['watsapp_intro_message'] = Setting.objects.get_or_create(
            key='watsapp_intro_message',
            defaults={'key': 'watsapp_intro_message',
                      'value': 'مدیریت سایت فیاتر'},
        )[0].value

        settings['instagram'] = Setting.objects.get_or_create(
            key='instagram',
            defaults={'key': 'instagram',
                      'value': 'Fiater'},
        )[0].value

        settings['contact_ua_WatsApp'] = Setting.objects.get_or_create(
            key='contact_ua_WatsApp',
            defaults={'key': 'contact_ua_WatsApp',
                      'value': 'https://wa.me/989021616483'},
        )[0].value

    return {'settings': settings}
