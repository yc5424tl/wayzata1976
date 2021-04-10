from wayzata76_web.models import Gallery


def galleries(request):
    return {
        "galleries": Gallery.objects.all(),
        "reunion_galleries": Gallery.objects.filter(section=("REUNIONS", "Reunions")).all(),
        "student_life_galleries": Gallery.objects.filter(section=("STUDENT_LIFE", "Student Life")).all(),
        "stomping_ground_galleries": Gallery.objects.filter(section=("STOMPING_GROUNDS", "The Stomping Grounds")).all(),
    }
