import graphene
from graphene_django.types import DjangoObjectType,ObjectType
from .models import Course, Student

# Create a GraphQL type for the Course model
class CourseType(DjangoObjectType):
    class Meta:
        model = Course

# Create a GraphQL type for the Student model
class StudentType(DjangoObjectType):
    class Meta:
        model = Student


# Create a Query type
class Query(ObjectType):
    student = graphene.Field(StudentType, id=graphene.Int())
    course = graphene.Field(CourseType, id=graphene.Int())

    students = graphene.List(StudentType)
    courses= graphene.List(CourseType)

    def resolve_student(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Student.objects.get(pk=id)

        return None

    def resolve_course(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Course.objects.get(pk=id)

        return None

    def resolve_students(self, info, **kwargs):
        return Student.objects.all()

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()




class CourseInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    year_of_publication = graphene.Int()

class StudentInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    courses = graphene.List(CourseInput)



# Create mutations for course
class CreateCourse(graphene.Mutation):
    class Arguments:
        input = CourseInput(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        course_instance = Course(
            title=input.title,
            year_of_publication=input.year_of_publication
        )
        course_instance.save()
        return CreateCourse(ok=ok, course=course_instance)

class UpdateCourse(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CourseInput(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        course_instance = Course.objects.get(pk=id)
        if course_instance:
            ok = True
            course_instance.title = input.title
            course_instance.year_of_publication = input.year_of_publication
            course_instance.save()
            return UpdateCourse(ok=ok, course=course_instance)
        return UpdateCourse(ok=ok, course=None)




class CreateStudent(graphene.Mutation):
    class Arguments:
        input = StudentInput(required=True)

    ok = graphene.Boolean()
    student = graphene.Field(StudentType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        courses_array = []
        for item_course in input.courses:
            course = Course.objects.get(pk=item_course.id)
            if course is None:
                return CreateStudent(ok=False, student=None)
            courses_array.append(course)
        student_instance = Student(
            name=input.name
        )
        student_instance.save()
        student_instance.courses.set(courses_array)
        return CreateStudent(ok=ok, student=student_instance)


class UpdateStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = StudentInput(required=True)

    ok = graphene.Boolean()
    student = graphene.Field(StudentType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        student_instance = Student.objects.get(pk=id)
        if student_instance:
            ok = True
            courses_array = []
            for item_course in input.courses:
                course = Course.objects.get(pk=item_course.id)
                if course is None:
                    return CreateStudent(ok=False, student=None)
                courses_array.append(course)
            student_instance.name = input.name
            student_instance.save()
            student_instance.courses.set(courses_array)
            return UpdateStudent(ok=ok, student=student_instance)
        return UpdateStudent(ok=ok, student=None)


class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
