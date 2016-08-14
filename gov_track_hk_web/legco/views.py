from django.shortcuts import render
from django.db.models import Count
from legco.models import Individual, Party, NewsArticle, IndividualVote, Vote, VoteSummary, Bill,  MeetingSpeech, MeetingHansard, FinanceMeetingItem, FinanceMeetingItemEvent, FinanceMeetingResult, Question
from datetime import date, datetime
from django.db.models import Q
from legco.models import MeetingSpeech, MeetingPersonel, MeetingHansard
# Create your views here.


def individual_view(request, pk):
    individual = Individual.objects.prefetch_related('party').get(pk=pk)
    personel_ids = MeetingPersonel.objects.filter(individual__pk = pk).values('id')
    absent_total =  MeetingHansard.objects.filter(members_absent__pk__in = personel_ids).count()
    present_total =  MeetingHansard.objects.filter(members_present__pk__in = personel_ids).count()
    question_total = Question.objects.filter(individual__pk = pk).count()
    related_news = NewsArticle.objects.filter(individuals__id = pk)[0:20]
    speech_total = MeetingHansard.objects.filter(speeches__individual__pk = pk).count()
    latest_speeches = MeetingHansard.objects.filter(speeches__individual__pk = pk).values_list('speeches__text_ch', 'date', 'pk', 'speeches__sequence_number').order_by('-date')[0:20]
    return render(request, 'legco/individual.html', {'nbar': 'party', 'tbar':'legco', 'individual': individual, 'related_news': related_news, 'present_total': present_total, 'absent_total': absent_total, 'question_total': question_total, 'latest_speeches': latest_speeches, 'speech_total': speech_total})

def index_view(request):
    return render(request, 'legco/index.html', {'nbar': 'home', 'tbar':'legco'})

def all_votes_view(request):
    return render(request, 'legco/vote.html', {'nbar': 'vote', 'tbar': 'legco'})

def vote_detail_view(request, pk):
    vote = Vote.objects.prefetch_related('meeting').prefetch_related('motion').get(pk = pk)
    individual_votes = IndividualVote.objects.prefetch_related('individual').filter(vote__id = pk)
    summaries = VoteSummary.objects.filter(vote__id = pk)
    yes_count = 0
    no_count = 0
    present_count = 0
    overall_result = ""
    for summary in summaries:
        yes_count += summary.yes_count
        no_count  += summary.no_count
        present_count += summary.yes_count + summary.no_count + summary.abstain_count
        if summary.summary_type == VoteSummary.OVERALL:
            overall_result = summary.result
    abstain_count = len(individual_votes) - yes_count - no_count - 1
    meeting = MeetingHansard.objects.get(Q(date__year = vote.date.year) & Q(date__month = vote.date.month) & Q(date__day = vote.date.day))
    return render(request, 'legco/vote_detail.html', {'nbar': 'meeting', 'tbar': 'legco', 'vote': vote, 'individual_votes': individual_votes, 'summaries': summaries, 'yes_count': yes_count, 'no_count': no_count, 'abstain_count': abstain_count, 'meeting': meeting, 'overall_result': overall_result})

def party_view(request, pk):
    party = Party.objects.get(pk = pk)
    related_news = NewsArticle.objects.filter(parties__id = pk)[0:20]
    individuals = Individual.objects.filter(party__id = pk)
    return render(request, 'legco/party.html', {'party': party, 'individuals': individuals, 'nbar':'party', 'tbar': 'legco', 'related_news': related_news})

def all_parties_view(request):
    parties = Party.objects.all()
    return render(request, 'legco/all_parties.html', {'parties': parties, 'nbar': 'party', 'tbar': 'legco'})

def all_bills_view(request):
    return render(request, 'legco/bill.html', {'nbar': 'bill', 'tbar': 'legco'})

def bill_detail_view(request, pk):
    bill = Bill.objects.prefetch_related('committee').prefetch_related('first_reading').prefetch_related('second_reading').prefetch_related('third_reading').get(pk=pk)
    bill_committee_individuals = [i for i in bill.committee.individuals.all()]
    first_reading_meetings = []	 
    first_reading_dates = [bill.first_reading.first_reading_date, bill.first_reading.first_reading_date_2]
    second_reading_dates = [bill.second_reading.second_reading_date, bill.second_reading.second_reading_date_2, bill.second_reading.second_reading_date_3, bill.second_reading.second_reading_date_4, bill.second_reading.second_reading_date_5]
    third_reading_dates = [bill.third_reading.third_reading_date]
    related_meetings = MeetingHansard.objects.filter(date__in = first_reading_dates + second_reading_dates + third_reading_dates).order_by('date')
    first_reading_meetings = [meeting for meeting in related_meetings if meeting.date in [f.date() for f in first_reading_dates]]
    second_reading_meetings = [meeting for meeting in related_meetings if meeting.date in [f.date() for f in second_reading_dates]]
    third_reading_meetings = [meeting for meeting in related_meetings if meeting.date in [f.date() for f in third_reading_dates]]
    return render(request, 'legco/bill_detail.html', {'nbar': 'bill', 'tbar': 'legco', 'bill': bill, 'bill_committee_individuals': bill_committee_individuals, 
            'first_reading_meetings': first_reading_meetings,
            'second_reading_meetings': second_reading_meetings,
            'third_reading_meetings': third_reading_meetings,
        })

def all_questions_view(request, keyword=""):
    return render(request, 'legco/questions.html', {'nbar': 'question', 'tbar': 'legco', 'search_keyword': keyword})

def question_detail_view(request, pk):
    question = Question.objects.prefetch_related('individual').get(pk = pk)
    keywords = [k.keyword for k in question.keywords.all()]
    return render(request, 'legco/question_detail.html', {'nbar': 'question', 'tbar': 'legco', 'question': question, 'keywords':keywords})


def hansard_view(request, pk):
    meeting = MeetingHansard.objects.prefetch_related('speeches').prefetch_related('speeches__individual').get(pk=pk)
    present = [p for p in meeting.members_present.all()]
    absent =  [p for p in meeting.members_absent.all()]
    public = [p for p in meeting.public_officers.all()]
    clerks = [p for p in meeting.clerks.all()]
    speeches = [s for s in meeting.speeches.all() if s.title_ch != "" or s.bookmark.startswith("EV")]
    votes = Vote.objects.prefetch_related('meeting').prefetch_related('motion').filter(Q(date__year = meeting.date.year) & Q(date__month = meeting.date.month) & Q(date__day = meeting.date.day))
    print len(votes)
    for speech in speeches:
        speech.est_min = int(len(speech.text_ch) * 0.012)
        speech.text_ch_short = speech.text_ch[0:100]
        speech.text_ch_more = speech.text_ch[100:]

    return render(request, 'legco/meeting.html', {'meeting': meeting, 'speeches': speeches, 'clerks': clerks, 'public': public, 'absent': absent, 'present': present, 'nbar':'meeting', 'tbar': 'legco', 'votes':votes})


def finance_item_view(request, pk):
    item = FinanceMeetingItem.objects.get(pk=pk)
    events = FinanceMeetingItemEvent.objects.prefetch_related('vote').filter(item__pk = pk).order_by('-date')
    return render(request, 'legco/fin_item.html', {'nbar':'meeting', 'tbar': 'legco', 'item': item, 'events': events})


def fc_result_view(request, pk):
    meeting = FinanceMeetingResult.objects.get(pk=pk)
    events = FinanceMeetingItemEvent.objects.prefetch_related('vote').prefetch_related('item').filter(result__pk = meeting.id).order_by('-date')
    return render(request, 'legco/fc_result.html', {'nbar':'meeting', 'tbar': 'legco', 'events': events, 'meeting': meeting})

def open_data_view(request):
    return render(request, 'legco/opendata.html', {'nbar': 'opendata', 'tbar': 'legco'})

def meeting_view(request):
    return render(request, 'legco/meetings.html', {'nbar': 'meeting', 'tbar': 'legco'})



