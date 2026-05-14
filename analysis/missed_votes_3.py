#!script

import sys, csv

from django.db.models import Q
from person.models import *
from vote.models import *

stats = { }

votes = Voter.objects.filter(
  vote__congress=sys.argv[1],
  vote__chamber=CongressChamber.by_key(sys.argv[2]),
  voter_type=VoterType.member, # VP can't be absent
  person_role__current=True,
)
if len(sys.argv) > 3:
	votes = votes.filter(vote__created__gte=sys.argv[3])
if len(sys.argv) > 4:
	votes = votes.filter(vote__created__lte=sys.argv[4])

# When searching on "Present" votes, only include votes were aye/no were possible
# (i.e. exclude call by states and quorum calls etc).
#substantive_votes = Vote.objects.filter(Q(options__key="+") | Q(options__key="-"))
#votes = votes.filter(vote__in=substantive_votes)

for vv in votes.order_by('vote__created').values('person', 'person_role', 'option__key', 'vote__created'):
	d = stats.setdefault(vv['person'], { "total": 0, 'missed': 0, "roles": set(), "first": vv['vote__created'], "lastvote": None })
	d['total'] += 1
	if vv['option__key'] == "0":
		d['missed'] += 1
	else:
		d['lastvote'] = vv['vote__created']
	d['roles'].add(vv['person_role'])
	d['last'] = vv['vote__created']

w = csv.writer(sys.stdout)
w.writerow(["congress", "chamber", "id", "name", "eligible", "missed", "first eligible", "last eligible", "last vote"])
people = Person.objects.in_bulk(stats.keys())
roles = PersonRole.objects.in_bulk( sum([list(stat['roles']) for stat in stats.values()], []) )
stats = sorted(stats.items(), key = lambda kv : kv[1]['missed']/float(kv[1]['total']))
for person, stats in stats:
	people[person]._roles = { roles[r] for r in stats['roles'] }
	w.writerow([ sys.argv[1], sys.argv[2], person, get_person_name(people[person], firstname_position='before'),
	    stats['total'], stats['missed'], stats['first'], stats['last'], stats['lastvote'] ])
