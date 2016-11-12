from django.conf.urls import url
from mainapp.utils.custom_router import HybridRouter
from mainapp.api import apiv1_methods as apiv1


router = HybridRouter()

# APIViews:
router.add_api_view("User Login view",
                    url(r'^auth/login/$', apiv1.LoginAPIView.as_view()))

router.add_api_view("User REGISTRATION",
                    url(r'^auth/register/$', apiv1.RegisterAPIView.as_view()))

router.add_api_view("User Schedule for Today",
                    url(r'^get_user_schedule/$', apiv1.TodayScheduleView.as_view()))

router.add_api_view("User Schedule for current week",
                    url(r'^get_user_weekly_schedule/$', apiv1.WeeklyScheduleView.as_view()))

router.add_api_view("User Schedule for NEXT week",
                    url(r'^get_user_next_week_schedule/$', apiv1.NextWeeklyScheduleView.as_view()))

router.add_api_view("Show all the students for the given group",
                    url(r'^get_students_group_list/$', apiv1.GroupStudentListView.as_view()))

router.add_api_view("Show student discipline results by date range",
                    url(r'^get_st_dsp_result/$', apiv1.StudentClassJournalView.as_view()))

router.add_api_view("Get student classes for semester",
                    url(r'^get_students_disciplines/$', apiv1.ListOfDisciplinesView.as_view()))

router.add_api_view("Get Faculty group structure",
                    url(r'^get_faculties_structure/$', apiv1.ListFacultyView.as_view()))

router.add_api_view("Add or update student journal",
                    url(r'^post_st_journal/$', apiv1.StudentJournalInstanceView.as_view()))

router.add_api_view("Get current groups that professor is teaching",
                    url(r'^get_teaching_groups/$', apiv1.GroupsListView.as_view()))
