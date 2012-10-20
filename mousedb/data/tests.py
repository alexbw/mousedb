"""This file contains tests for the data application.

These tests will verify generation of new experiment, measurement, assay, researcher, study, treatment, vendor, diet, environment, implantation, transplantation and pharnaceutical objects.
"""
import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.data.models import Study, Diet, Environment, Researcher, Treatment, Transplantation, Pharmaceutical, Implantation
from mousedb.animal.models import Strain, Animal

MODELS = [Study]

class BasicTestCase(TestCase):
    '''This class factors out the TestcCase setup and Teardown code.'''

    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

class StudyModelTests(BasicTestCase):
    """Test the creation and modification of Study objects."""

    def test_create_study_minimal(self):
        """This is a test for creating a new study object, with only the minimum being entered.  It also verifies that unicode is set correctly."""
        new_study = Study(description = "Effects of x on y")
        new_study.save()
        self.assertEquals(new_study.__unicode__(), u'Effects of x on y')

    def test_create_studey_detailed(self):
        """This is a test for creating a new study object, with all fields being entered.  It also verifies that unicode is set correctly.  This test is dependent on the ability to create a new Strain object (see animal.tests.StrainModelTests.test_create_minimal_strain)."""
        new_study = Study(
            description = "Effects of x on y",
            start_date = datetime.date.today(),
            stop_date = datetime.date.today(),
            notes = "some notes on this strain"
            )
        new_study.save()
        new_study.strain.create(Strain='test_strain')
        self.assertEquals(new_study.__unicode__(), u'Effects of x on y')

    def test_study_absolute_url(self):
        """This test verifies that the absolute url of a study object is set correctly.  This study is dependend on a positive result on test_create_study_minimal."""
        test_study = Study(description = "Effects of x on y")
        test_study.save()
        self.assertEquals(test_study.get_absolute_url(), '/studies/1/')

class StudyViewTests(BasicTestCase):
    """These tests test the views associated with Study objects."""

    fixtures = ['test_study',]

    def test_study_list(self):
        """This test checks the status code, and templates for study lists."""
        response = self.client.get('/study/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_list.html')

    def test_study_detail(self):
        """This test checks the view which displays a study detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_detail.html')
        self.assertTemplateUsed(response, 'experiment_list_table.html')

    def test_study_new(self):
        """This test checks the view which displays a study creation page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_form.html')

    def test_study_edit(self):
        """This test checks the view which displays a study edit page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_form.html')


    def test_study_delete(self):
        """This test checks the view which displays a study detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'confirm_delete.html')
				
class TreatmentModelTests(BasicTestCase):
    '''These tests test the functionality of :class:`~mousedb.data.models.Treatment` objects.'''
    
    fixtures = ['test_diet', 'test_environment', 'test_researcher', 
    'test_animals', 'test_strain', 'test_vendor', 'test_study', 'test_transplantation',
    'test_pharmaceutical','test_implantation']
    
    def test_create_treatment_minimum(self):
        '''This test creates a :class:`~mousedb.data.models.Treatment` with the required information only.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1))
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        self.assertEqual(test_treatment.pk, 1) #presumes no models loaded in fixture data
        
    def test_create_treatment_all(self):
        '''This test creates a :class:`~mousedb.data.models.Treatment` with all information entered.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1),
            study = Study.objects.get(pk=1),
            transplantation = Transplantation.objects.get(pk=1),
            notes = "Some notes about this test treatment."
            )
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        test_treatment.pharmaceutical.add(Pharmaceutical.objects.get(pk=1))  
        test_treatment.implantation.add(Implantation.objects.get(pk=1))                
        self.assertEqual(test_treatment.pk, 1) #presumes no models loaded in fixture data       
        
    def test_treatment_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.data.models.Treatment`.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1))
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        self.assertEqual(test_treatment.__unicode__(), "Test Treatment")  
        
    def test_treatment_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.data.models.Treatment`.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1))
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        self.assertEqual(test_treatment.get_absolute_url(), "/treatment/1")

class TreatmentViewTests(BasicTestCase):
    """These tests test the views associated with Treatment objects."""

    fixtures = ['test_treatment','test_study', 'test_diet', 'test_environment', 'test_vendor']

    def test_treatment_detail(self):
        """This test checks the view which displays a treatment-detail page.  
        
        It checks for the correct templates and status code."""        

        test_response = self.client.get('/treatment/1/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('treatment' in test_response.context)            
        
        #test templates
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'treatment_detail.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')
        self.assertTemplateUsed(test_response, 'menu_script.html')              
        
        #test object attributes
        self.assertEqual(test_response.context['treatment'].pk, 1)
        self.assertEqual(test_response.context['treatment'].treatment, u'Test Treatment')
        self.assertEqual(test_response.context['treatment'].notes, u'Some Notes')
        self.assertEqual(test_response.context['treatment'].diet.__unicode__(), u'Test Diet')
        
        #test that an incorrect id gives a 404
        wrong_test_response = self.client.get('/treatment/101/')
        self.assertEqual(wrong_test_response.status_code, 404)
        
    def test_treatment_list(self):
        """This tests the treatment-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/treatment/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('treatment_list' in test_response.context) 

        #test templates
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'treatment_list.html')
        self.assertTemplateUsed(test_response, 'menu_script.html')        

        #test object attributes
        self.assertEqual(test_response.context['treatment_list'][0].pk, 1)
        self.assertEqual(test_response.context['treatment_list'][0].treatment, u'Test Treatment')
        self.assertEqual(test_response.context['treatment_list'][0].notes, u'Some Notes')
        self.assertEqual(test_response.context['treatment_list'][0].diet.__unicode__(), u'Test Diet')
