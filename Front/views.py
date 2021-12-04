from builtins import print

from django.views import View
from django.shortcuts import render, get_object_or_404
from Category.models import Category
from Coupon.models import Coupon
from Setting.models import Setting
from Episode.models import Episode
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, Http404
from Subscription.models import Subscription, Type
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from Gateway.views import CalculateCouponAmount
from .helpers import PersianizeAmount
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta

User = get_user_model()

def paginate(paginator, page , search_word=None):
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    html = render_to_string(
        template_name="Front/partials/episodes.html",
        context={'episodes': objects , 'search_word' : search_word}
    )
    data_dict = {"episodes": html}
    return data_dict


def Search(search_word):
    query = Q(title__icontains=search_word) | Q(actors__icontains=search_word) | \
            Q(genre__icontains=search_word) | Q(category__name__icontains=search_word)

    videos = Episode.objects.filter(query).distinct().order_by('-created_at')
    return videos


##############################################################

class Index(View):
    def get(self, request):
        context = {}

        if 'search' in request.GET:
            episodes = Search(request.GET['search'])
            context['search_word'] = request.GET['search']

            page = request.GET.get('page', 1)
            paginator = Paginator(episodes, settings.PAGINATION_NUMBER)

            if request.is_ajax():
                data_dict = paginate(paginator, page , context['search_word'])
                return JsonResponse(data_dict, safe=False)

            context['episodes'] = paginator.page(1)
            return render(request, 'Front/search_result.html', context)


        context = {
            'categories': Category.objects.all(),
            'advertise_text': Setting.objects.get_or_create(
                key='advertise_text',
                defaults={'key': 'advertise_text',
                          'value': 'تماشای نامحدود برترین فیلم تئاتر های روز دنیا و مجموعه های آموزشی هفت هنر، با زیرنویس تخصصی فارسی و اینترنت نیم بها، بصورت آنلاین تنها با یک اشتراک در بازه زمانی مشخص'},
            )[0].value,

            'embed_advertise_image': Setting.objects.get_or_create(
                key='embed_advertise_image',
                defaults={'key': 'embed_advertise_image',
                          'value': '/static/front/img/tv.png'},
            )[0].value,

            'embed_advertise_gif': Setting.objects.get_or_create(
                key='embed_advertise_gif',
                defaults={'key': 'embed_advertise_gif',
                          'value': '/static/front/img/fiatre.gif'},
            )[0].value,
        }
        return render(request, 'Front/index.html', context)


class Account(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        context = {
            'user': request.user
        }

        return render(request, 'Front/account.html', context)


class About_us(TemplateView):
    template_name = 'Front/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['about_title'] = Setting.objects.get_or_create(
            key='about_title',
            defaults={'key': 'about_title',
                      'value': 'درباره فیاتر'},
        )[0].value

        context['about_text'] = Setting.objects.get_or_create(
            key='about_text',
            defaults={'key': 'about_text',
                      'value': """<p><span class="fontstyle2">سلام!<br>
                    شبی از شبهای پاییزی سال یک هزار و سیصد و نود و هشت ( ۱۳۹۸ ) به این نتیجه رسیدیم که جای خالی یک </span><span
                    style="color: #9d1f20;"><strong><a style="color: #9d1f20;"
                                                       href="https://en.wikipedia.org/wiki/Video_on_demand" target="_blank"
                                                       rel="noopener"><span
                    class="fontstyle3">VOD </span></a></strong></span><span class="fontstyle2">آموزشی در زمینه سینما، تئاتر و هنرهای تجسمی خالیه.<br>
                    قبلنا تو پیج اینستاگرام از ما درخواست محتوا با زیرنویس فارسی میکردن، ما هم که سرمون درد میکنه برای این کارا ….</span><span
                    class="fontstyle2"><br>
                    چی شد که اسمشو گذاشتیم فیاتر؟! فیلم و تئاتر و ترکیب کردیم و به <span style="color: #9d1f20;"><strong><a
                        style="color: #9d1f20;" href="https://fiatre.ir/">فیاتر</a></strong></span> رسیدیم!<br>
                    سرتونو درد نیاریم … این سایتو زدیم تا کل علاقه مندا و هنر دوستای کشورمون به منابع خوب و درجه یکه آموزشی دسترسی داشته باشن. به هر حال چرخ سایت باید بچرخه. راستی ما برای اینکه کارمون قانونی باشه مجوزهایی که لازم هست رو گرفتیم و کلیه فعالیت هامون در چهارچوب قوانین کشورمون هست. بلانسبت شما! اگر خدایی نکرده کسی بخواد از مطالب ما سو استفاده و بهره برداری کنه، مجبوریم علی رغم میل باطنیمون تحت پیگرد قانونی قرارش بدیم.<br>
                    اینم بگم که خیلی دوست داریم نظرها و پیشنهاداتونو بشنویم،خودتون که راه ارتباط باهامونو بلدید،پس باهامون در ارتباط باشید.<br>
                   </span></p>"""},
        )[0].value

        return context


class Terms(TemplateView):
    template_name = 'Front/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['terms_title'] = Setting.objects.get_or_create(
            key='terms_title',
            defaults={'key': 'terms_title',
                      'value': 'قوانین فیاتر'},
        )[0].value

        context['terms_text'] = Setting.objects.get_or_create(
            key='terms_text',
            defaults={'key': 'terms_text',
                      'value': """<p>کاربر گرامی</p>
                                <p>فیاتر سرویس خود را تحت شرایط و مقررات این توافقنامه در اختیار شما می گذارد و شما به عنوان کاربران این سرویس ملزم به رعایت مفاد مذکور در این توافقنامه که ممکن است در آیینده تغییر کند هستید. این سرویس با نام تجاری
                                    ” <a href="https://fiatre.ir/">فیاتر</a> ” ثبت گردیده است و از حق کپی رایت برخوردار است. اگر در سایت های دیگر با موارد نقض کپی رایت فیاتر مواجه شدید، لطفا آن را به سرویس پشتیبانی ما اطلاع دهید. اعمال غیر قانونی و مغایر
                                    با قوانین موضوعه جمهوری اسلامی ایران به هر نحو ممکن ممنوع است. تمامی محتواهای ارایه شده در سرویس فیاتر در چارچوب قوانین و مقررات جمهوری اسلامی ایران می باشد.</p>
                                <p>استفاده از سرویس فیاتر هیچگونه حقی را برای کاربران در ارتباط با مالکیت فیلم ها و به طور کلی هر محتوای ارائه شده و شما انتشار یا پخش عمومی آنها چه از طریق سرویس فیاتر و چه از طرق دیگر ایجاد نمی کند. مسلم است با پرداخت مبلغ،
                                    می توانید خدمات خریداری شده را در بازه زمانی مشخص شده مشاهده کنید، اما مالک این محتوا نخواهید شد و اجازه دانلود و بازنشر آن را ندارید.فیاتر حق پیگیری و شکایت در مراجع ذیصلاح را در صورت دانلود و باز پخش محتوای فیاتر
                                    را برای خود محفوظ میدارد.</p>
                                <p>برای دسترسی به نمایش محتوای مورد نظر، کاربر باید اقدام به خرید اشتراک نماید. خرید اشتراک در واقع به منزله خرید دسترسی به محتواهای فیاتر می باشد. در صورت مشاهده هرگونه اقدام غیر متعارف برای دسترسی به اشتراک، خرید و ورود،فیاتر
                                    این حق را دارد که این اقدامات غیرمجاز را متوقف و در ادامه اشتراک کاربر را لغو کند. تعداد محتواهایی که کاربران با خرید اشتراک به آنها دسترسی پیدا می کنند ممکن است پیش از پایان مدت اعتبار اشتراک، تغییر یافته و فیلم هایی
                                    به مجموع محتواها اضافه یا از آن حذف گردد.</p>
                                <p>در حال حاضر کاربران فیاتر می توانند با اینترنت نیم بها از تمامی خدمات سرویس فیاتر بهرهمند شوند، اما در صورت استفاده غیرمتعارف و مخرب شما به عنوان کاربر خانگی، فیاتر این حق را برای خود قائل است تا برابر ضوابط مرسوم بر شما
                                    نحوه و میزان استفاده کاربران، مجددا محدودیتهایی را اعمال نماید که در این صورت قواعد جدید متعاقبا خدمت اعلام خواهد شد. فیاتر هیچ مسئولیتی در قبال مشکلات سخت افزاری یا نرم افزاری یا هر زیان دیگری که در نتیجه استفاده از
                                    این سرویس متوجه کامپیوتر یا تلفن هوشمند یا … کاربر یا دیگران شود ندارد یا فیاتر این حق را دارد که در صورت نیاز تغییراتی در قوانین ایجاد کرده یا مانع دسترسی به بعضی از قسمت های سرویس همه سرویس بطور موقت یا دائمی شود.</p>
                                <p>در قسمت مربوط به نظرات کاربران، انتشار مطالب خلاف یا نقض کننده قوانین جمهوری اسلامی ایران، مضر، تهدید کننده، توهین آمیز، غیر اخلاقی، افترا آمیز و مبتذل و همچنین مطالبی که به نژاد، گروه یا دسته خاصی از مردم توهین کند، ممنوع
                                    است در قسمت مربوط به نظرات کاربران، قرار دادن لینک هایی به سایت های غیر قانونی، غیر اخلاقی یا مبتذل و همینطور سایت هایی که به هر نحو مناسبات فرهنگی، اخلاقی، عرفی یا قانونی جامعه را زیر پا می گذارند یا با قوانین جمهوری
                                    اسلامی ایران مغایرند، ممنوع است.</p>
                                <p>محتواهای موجود توسط یک تهیه کننده یا کمپانی تئاتر تهیه شده است. فیاتر تنها یک بستر نمایش این محتواها بوده و نقشی در تولید آنها نداشته، از اینرو مسئولیتی در قبال محتوای ارائه شده ندارد. درصورت بروز شرایط فورس ماژور )مانند
                                    سیل، زلزله، بلایای طبیعی و…( و پیش آمدهای خارج از کنترل فیاتر که منجر به قطع سرویس و ارائه خدمات شود، تا زمان برطرف شدن مشکل، این قرارداد معلق خواهد شد. این توافقنامه مشروعیت و اعتبار خود را از قوانین حاکم بر جمهوری
                                    اسلامی ایران کسب می کند.</p>
                                <p>براساس توافق صورت گرفته بین فیاتر و تمامی اپراتورها شرایطی مهیا شده تا اینترنت مصرف شده برای تماشا و دانلود فیلم در سرویس فیاتر برای کاربران این اپراتورها و تامین کنندگان اینترنت نیم بها محاسبه شود. برمبنای همین توافق مسئولیت
                                    پخش آنلاین محتواها به عهده فیاتر و مسئولیت برقراری ارتباط اینترنتی و نیم بها بودن حجم مصرفی کاربران به عهده اپراتورها خواهد بود.&nbsp; در صورتی که هنگام تماشای فیلم در سرویس فیاتر، فیلترشکن شما روشن باشد ترافیک اینترنت
                                    برای شما تمام بها محاسبه خواهد شد.</p>
                                <p>ترافیک اینترنت برای تماشای محتوا در فیاتر با ترافیک نیم بها محاسبه می شود اما در صورتی که فیلتر شکن، تلگرام، مرورگرها و سایر نرمافزارهای موجود در تلویزیون هوشمند، تبلت و گوشی تلفن همراه شما باز یا در حال دانلود کردن باشند
                                    به طور طبیعی از حجم اینترنت شما کسر خواهد شد و این حجم مصرفی هیچ ارتباطی با تماشای فیلم در سرویس فیاتر نخواهد داشت. فیاتر این اختیار را دارد، هنگام پخش فیلم به فراخور زمان و محتوا، برای کاربر تبلیغ نمایش دهد.</p>
                                <p>فیاتر جهت ارائه بهتر سرویس خود و اطلاع رسانی در خصوص طرح های ویژه و پیشنهاد تماشای فیلم های جدید و …، ممکن است از طریق ایمیل یا شماره تلفن همراه ثبت شده، اقدام به ارسال اطلاعاتی برای کاربران نماید.</p>"""},
        )[0].value

        return context


class Faq(TemplateView):
    template_name = 'Front/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['faq_text'] = Setting.objects.get_or_create(
            key='faq_text',
            defaults={'key': 'faq_text',
                      'value': """<p><strong>۱. چگونه در سایت فیاتر ثبت نام کنم؟</strong></p>
                                <p>ثبت نام در فیاتر با شماره تلفن همراه و انتخاب یک رمز عبور انجام می گیرد. پس از وارد کردن شماره تلفن همراه،انتخاب رمز ورود و تکرار آن ثبت نام شما کامل می گردد.</p>
                                <p><strong>۲. چطور می توانم اشتراک خریداری کنم؟</strong></p>
                                <p>پس از ثبت نام،به صفحه خرید اشتراک مراجعه کرده،پلن مورد نظر خود را انتخاب،وارد درگاه پرداخت شده و با استفاده از کارتهای بانکی متصل به شبکه شتاب هزینه اشتراک خود را پرداخت نمایید،کار تمام است و می توانید از تمامی ویدئو های موجود استفاده بفرمایید.
                                </p>
                                <p><strong>٣. چرا باید برای تماشای فیلم ها اشتراک تهیه کنم؟</strong><strong></strong></p>
                                <p>حقوق صاحبین اثر تمامی فیلم های آموزشی،فیلم تئاترها و مستندهای موجود در فیاتر(ترجمه،زیرنویس و قابل پخش شدن) بصورت کاملا قانونی خریداری و در فیاتر قرار داده شده اند. شما با پرداخت مبلغ مربوط به خرید اشتراک در عین اینکه فیلم را قانونی تماشا می کنید، از صاحبین اثر نیز حمایت می کنید و باعث تولید محتوای با کیفیت  خواهید شد. ضمنا شما با خرید اشتراک در بازه زمانی مشخص شده، به تمامی محتوای فیاتر دسترسی خواهید داشت و میتوانید به دفعات تماشا کنید.</p>
                                <p><strong>۴. آیا می توانم فیلم ها را دانلود کنم؟</strong><strong></strong></p>
                                <p>بله در حال حاضر امکان تماشای آنلاین و دانلود با اینترنت نیم بها،برای مشترکین فیاتر فراهم گردیده است.</p>
                                <p><strong>۵. با خرید اشتراک فیاتر ترافیک مصرفی اینترنت&nbsp; من نبم بها محاسبه خواهد شد؟</strong><strong></strong></p>
                                <p>بله.ترافیک مصرفی تمامی مشترکینی که با آی پی داخل کشور وارد سایت شده اند نیم بها محاسبه خواهد شد.بدیهی است در صورت استفاده از هرگونه فیلتر شکن و نرم افزار تغییر آی پی اینترنت شما تمام بها محاسبه خواهد شد.</p>
                                <p><strong>۶. در هنگام پخش فیلم ها از فیاتر، ارور دریافت می کنم. مشکل از کجاست؟</strong><strong></strong></p>
                                <p>چنانچه حین پخش با هرگونه خطا مواجه شدید به صفحه پشتیبانی &nbsp;مراجعه و مشکل خود را مطرح نمایید تا در اولین فرصت مشکل را بررسی و برطرف کنیم.</p>
                                <p><strong>۷. اشتراک من فعال شده است اما فیلم ها برایم به نمایش در نمی آید؟</strong></p>
                                <p>قبل از ارتباط با واحد پشتیبانی یکبار بصورت کامل از حساب کاربری خود خارج و دوباره وارد شوید،درصورت حل نشدن مشکل آن را با واحد پشتیبانی در میان گذاشته تا در اسرع وقت مشکل شما را برسی و حل نمایند.</p>
                                <p><strong>۸. به صورت همزمان چند کاربر می توانند از اکانت یک شخص استفاده کنند و فیلم ببینند؟</strong><strong></strong></p>
                                <p>با یک ip می توان روی هر چند دستگاه که بخواهید به صورت همزمان فیلم تماشا کنید. اما در صورتی که با بیش از یک ip اقدام به تماشای فیلم کنید، خطای پخش همزمان دریافت خواهید کرد. ضمن اینکه به کاربران گرامی توصیه می شود اطلاعات
                                    کاربری خود را در اختیار دیگران قرار ندهند.</p>
                                <p><strong>۹. فیلم های فیاتر در تلویزیون هوشمند من پخش نمی شود. مشکل از کجاست؟</strong><strong></strong></p>
                                <p>چنانچه حین پخش با تلویزیون هوشمند با هرگونه مشکلی مواجه شدید، به صفحه پشتیبانی &nbsp;مراجعه و جزییات مشکل خود را مطرح نمایید. در نظر داشته باشید که ممکن است دستگاه شما، سیستم پخش فیلم در فیاتر را پشتیبانی نکند، اما سعی
                                    ما بر این است که راه حلی برای تمامی مشکلات شما پیدا کنیم.</p>
                                <p><strong>۱۰. در صورت بروز مشکل در خرید از فیاتر مانند فعال نشدن اشتراک و یا ثبت نشدن پرداخت، امکان پیگیری از چه طریقی وجود دارد؟</strong><strong></strong></p>
                                <p>چنانچه جهت خرید اشتراک اقدام کرده اید و مبلغی از حساب شما کم شده اما پرداخت صورت نگرفت، لطفا تا ۷۲ ساعت تامل بفرمایید تا مبلغ کسر شده به حساب شما بازگردد. پس از سپری شدن این مدت، چنانچه مبلغ به حساب شما واریز نگردید، می توانید شماره کارت بانکی که پرداخت با آن صورت گرفته،به همراه تاریخ خرید از طریق صفحه پشتیبانی ارسال کرده تا بررسی شود. اگر پرداخت در فیاتر برگشت خورده و مبلغ به حساب شما عودت داده نشده است، می بایست با پشتیبانی درگاه بانکی مورد نظر تماس بگیرید.
									در نظر داشته باشید مسئولیت استفاده و ورود به درگاه پرداخت با هرگونه فیلترشکن و نرم افزار تغییر آی پی متوجه شما می باشد و فیاتر هیچ گونه مسئولیتی در مورد عواقب کسر وجه و هک شدن حساب بانکی شما را توسط کلاه برداران اینترنتی نمی پذیرد.
                                </p>
                                <p>در نظر داشته باشید مسئولیت استفاده و ورود به درگاه پرداخت با هرگونه فیلتر شکن و نرم افزار تغییر آی پی متوجه شما می باشد و فیاتر هیچ گونه مسئولیتی در مورد عواقب کسر وجه و هک شدن حساب بانکی شما را توسط کلاه برداران اینترنتی
                                    نمی پذیرد.</p>
                                <p><strong>۱۱. کاربران مقیم خارج از کشور به چه ترتیب می توانند اشتراک فیاتر را تهیه کنند؟</strong><strong></strong></p>
                                <p>خرید اشتراک از فیاتر در حال حاضر تنها با کارت های بانکی شبکه شتاب ایرانی قابل خرید می باشد.</p>
                                <p><strong>۱۲ . محتوای جدید کِی اضافه می گردد؟</strong></p>
                                <p>سعی شده است بصورت هفتگی محتوای جدید در دسترس گاربران قرار بگیرد.</p>
                                <p><strong>۱۳. چطور می توانم از اضافه شدن محتوای جدید با خبر شوم؟</strong></p>
                                <p>با عضویت در صفحه شبکه اجتماعی فیاتر بخصوص اینستاگرام فیاتر می توانید در جریان تمامی اخبار سایت قرار بگیرید.</p>
                                <p><strong>۱۴. من علاقه مند هستم با تیم فیاتر همکاری کنم،آیا میتوانم همکار شما شوم؟</strong></p>
                                <p>بله.لطفا از طریق فرم تماس با ما توانایی ها و تخصص های خود را همراه با رزومه ارسال کرده تا در اولین فرصت برسی گردد.</p>
                                <p><strong>۱۵ . چرا فیلم تئاتر ایرانی در سایت قرار نمی دهید؟</strong></p>
                                <p>از آنجا که کیفیت فنی تصویر برداری و همچنین کیفیت آثار برای فیاتر بسیار حائز اهمیت می باشد در صورت معرفی و یافتن چنین آثاری حتما خریداری شده و در دسترس شما قرار خواهد گرفت.</p>
                                <p><strong>۱۶ . آیا می توانم پیشنهاد قراردادن محتوای خاصی دهم؟</strong></p>
                                <p>بله. پیشنهادات شما باعث بالا رفتن کیفیت فیاتر می شود،از قسمت تماس با ما پیشنهاد خود را با ما در میان بگذارید.</p>"""},
        )[0].value

        return context


class InternetConditions(TemplateView):
    template_name = 'Front/Internet_conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['Internet_conditions_text'] = Setting.objects.get_or_create(
            key='Internet_conditions_text',
            defaults={'key': 'Internet_conditions_text',
                      'value': """<p>
                            براساس توافق صورت گرفته بین فیاتر و تمامی اپراتورها شرایطی مهیا شده تا اینترنت مصرف شده برای
                            تماشای آنلاین در سرویس فیاتر برای کاربران این اپراتورها و تامین کنندگان اینترنت نیم بها
                            محاسبه شود. برمبنای همین توافق مسئولیت پخش آنلاین محتواها به عهده فیاتر و مسئولیت برقراری
                            ارتباط اینترنتی و نیم بها بودن حجم مصرفی کاربران به عهده اپراتورها خواهد بود. در صورتی که
                            هنگام تماشای فیلم در سرویس فیاتر، فیلترشکن شما روشن باشد ترافیک اینترنت برای شما تمام بها
                            محاسبه خواهد شد.
                            <br/>
                            <br/>
                            ترافیک اینترنت برای تماشای محتوا در فیاتر با ترافیک نیم بها محاسبه می شود اما در صورتی که
                            فیلتر شکن، تلگرام، مرورگرها و سایر نرم افزارهای موجود در تلویزیون هوشمند، تبلت و گوشی تلفن
                            همراه شما باز یا در حال دانلود کردن باشند به طور طبیعی از حجم اینترنت شما کسر خواهد شد و این
                            حجم مصرفی هیچ ارتباطی با تماشای فیلم در سرویس فیاتر نخواهد داشت.
                            <br/>
                            <br/>
                            – شرایط مصرف اینترنت نیم بها: در حال حاضر ترافیک مصرفی برای تمامی مشترکین اپراتور ها از
                            قبیل:همراه اول،ایرانسل،رایتل و… همچنین کلیه شرکت های ارائه دهنده اینترنت پر سرعت و یا
                            فیبرنوری از قبیل مخابرات،شاتل،های وب،آسیا تک،پارس آنلاین،صبا نت و… در تمام نقاط ایران نیم
                            بها محاسبه می گردد.
                            <br/>
                            <br/>
                            – شرایط مصرف اینترنت تمام بها: برای آن دسته از افرادی که در کشور های دیگر اقامت داشته و خارج
                            از مرز های ایران وارد وبسایت فیاتر می شوند ترافیک اینترنت تمام بها محاسبه می گردد.همچنین
                            افرادی که از هر نوع فیلتر شکن،نرم افزار تغییر آی پی و vpn استفاده کرده و همزمان وارد فیاتر
                            شوند اینترنت تمام بها محاسبه می گردد.
                        </p>"""},
        )[0].value

        return context

class Cat(View):
    def get(self, request, slug):
        context = {
            'category': get_object_or_404(Category, slug=slug)
        }

        context['episodes'] = Episode.objects.filter(category__slug=slug).order_by('-created_at')

        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['episodes'], settings.PAGINATION_NUMBER)

        if self.request.is_ajax():
            data_dict = paginate(paginator, page)
            return JsonResponse(data_dict, safe=False)

        context['episodes'] = paginator.page(1)
        return render(request, 'Front/category_episodes.html', context)


class EpisodeDetail(DetailView):
    template_name = 'Front/episode.html'
    slug_field = 'slug'
    model = Episode
    context_object_name = 'episode'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_episodes'] = self.object.category.episodes.exclude(slug=self.kwargs['slug'])[:6]
        return context


## Subscription ##

class SubscriptionPlans(LoginRequiredMixin, TemplateView):
    template_name = 'Front/Subscription-Plans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['plans'] = Type.objects.all()
        context['colors'] = ['plan1', 'featured', 'plan3']
        context['counter'] = 0

        return context


class SubscriptionBuy(LoginRequiredMixin, DetailView):
    template_name = 'Front/Subscription-Buy.html'
    slug_field = 'slug'
    model = Type
    context_object_name = 'type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['subscription_welcome_text'] = Setting.objects.get_or_create(
            key='subscription_welcome_text',
            defaults={'key': 'subscription_welcome_text',
                      'value': """<p>
                                <span>با خرید اشتراک به امکانات زیر دسترسی خواهید داشت:<br>تماشای نامحدود برترین فیلم تئاتر های روز دنیا و مجموعه های آموزشی هفت هنر، با زیرنویس تخصصی فارسی تنها با یک اشتراک در بازه زمانی مشخص.
					            <br>ترافیک مصرفی نیم بها برای تمامی اپراتورها و سرویس دهندگان اینترنت ایران.<br>امکان دانلود تمامی محتویات فیاتر و تماشای آن در زمانی که دسترسی به اینترنت ندارید.<br>پشتیبان فیاتر هفت روز هفته و در هر مرحله ای پاسخگوی سوالات شما می باشد.<br>از فیاتر لذت ببرید.</span>
                                </p>"""},
        )[0].value

        context['subscription_takhfif_code_text'] = Setting.objects.get_or_create(
            key='subscription_takhfif_code_text',
            defaults={'key': 'subscription_takhfif_code_text',
                      'value': """<p>
                                    ثبت کد تخفیف یا کد هدیه
                                    <br>
                                    جهت دریافت آخرین اخبار و اطلاعات،فیاتر را در صفحات اجتماعی دنبال کنید.
                                    </p>"""},
        )[0].value

        return context


class SubscriptionCheckCoupon(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            context = {
                'status': 'fail'
            }
            code = request.POST.get('code', None)
            amount = request.POST.get('amount', 0)

            if code:
                coupon = Coupon.objects.filter(code=code).first()
                if coupon:
                    today = timezone.now()
                    expiration = coupon.created_at + relativedelta(months=coupon.time)
                    if today > expiration:
                        context['errors'] = 'این کد تخفیف منقضی شده است!'

                    else:
                        try:
                            del request.session['coupon']
                        except:
                            pass
                        request.session['coupon'] = coupon.code

                        new_amount = CalculateCouponAmount(coupon.percent , int(amount))

                        context['message'] = 'کد تخفیف مورد نظر با موقیت ثبت شد.'
                        context['new_amount'] = PersianizeAmount(new_amount)
                        context['status'] = 'success'
                else:
                    context['errors'] = 'همچین کد تخفیفی وجود ندارد!'

            else:
                context['errors'] = 'لطفا کد تخفیف را وارد کنید!'

            return JsonResponse(context, safe=False)

        else:
            raise Http404


## Increase View CountiewCo
class EpisodesViewCountIncreaseView(LoginRequiredMixin , UpdateView):
    model = Episode
    success_url = '/'
    fields = ['view_count']

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.view_count += 1
        object.save()

        return JsonResponse({'status' : 'OK'}, safe=False)


## Watching
class WatchingStatusChangeView(LoginRequiredMixin , View):
    success_url = '/'

    def post(self, request, *args, **kwargs):
        request.user.is_watching = not request.user.is_watching
        request.user.save()

        return JsonResponse({'status' : 'OK'}, safe=False)


## DownloadCount
class DownloadCountView(LoginRequiredMixin , View):
    success_url = '/'

    def post(self, request):
        subscription_day = request.user.subscription.filter(status=True).last().created_at.date().day
        last_month = datetime.now() - relativedelta(months=1)
        last_user_downloads = request.user.user_downloads\
            .filter(created_at__range=(last_month.replace(day=subscription_day), datetime.now()))

        if last_user_downloads.count() >= 10:
            return JsonResponse({'status' : 'ERROR'} , status   =400, safe=False)

        request.user.user_downloads.create(episode_id=request.POST.get('episode'))
        request.user.save()
        return JsonResponse({'status' : 'OK'}, safe=False)