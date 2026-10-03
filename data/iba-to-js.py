import json,re
src=json.load(open('iba.json'))
RULES=[('M',r'ginger beer|ginger ale|cola|soda|^water'),
('L',r'liqueur|apricot brandy|peach brandy|cherry brandy|cherry sangue|cr.{1,3}me\s+de|cassis|dictine|curacao|triple sec|cointreau|grand marnier|maraschino|kahl|drambuie|amaretto|frangelico|b[ée]n[ée]dictine|chartreuse|falernum|campari|aperol|fernet|cynar|amaro|angostura|allspice|schnapps|galliano'),
('C',r'lemon|lime'),
('Y',r'syrup|nectar|honey|grenadine|cordial|donn|sugar cane juice'),
('J',r'juice|puree'),
('D',r'cream|egg|coffee|espresso'),
('W',r'vermouth|prosecco|champagne|wine|port|sherry|lillet|amontillado|palo cortado'),
('S',r'.')]
def cls(n):
    for k,r in RULES:
        if re.search(r,n,re.I): return k
# (slug, substring) -> (label, class, cl) estimated
EST={('americano','Soda'):('Soda water','M',3),('gin-fizz','Soda'):('Soda water','M',3),('fernandito','Cola'):('Cola','M',10),
('long-island-iced-tea','Cola'):('Cola','M',3),('mojito','Soda'):('Soda water','M',4),('ramos-fizz','Soda Water'):('Soda water','M',3),
('russian-spring-punch','Sparkling'):('Sparkling wine','W',6),('spritz','Soda'):('Soda water','M',3),('suffering-bastard','Ginger'):('Ginger beer','M',9),
('espresso-martini','Espresso'):('Espresso','D',3),('pisco-sour','Egg'):('Egg white','D',3),('bees-knees','Honey'):('Honey syrup','Y',1),
('monkey-gland','Absinthe'):('Absinthe','S',1.5),('monkey-gland','Grenadine'):('Grenadine','Y',1.5),('aviation','Violette'):('Crème de violette','L',0.5),
('brandy-crusta','Curacao'):('Curaçao','L',0.5),('brandy-crusta','Simple'):('Simple syrup','Y',0.5),('illegal','Maraschino'):('Maraschino','L',0.5),
('martinez','Maraschino'):('Maraschino','L',0.5),('vieux-carre','dictine'):('Bénédictine','L',0.5),('zombie','Grenadine'):('Grenadine','Y',0.5),
('mint-julep','Water'):('Water','M',1)}
CAT={'?':'Unforgettables','Contemporary Classics':'Contemporary','New Era':'New Era'}
def clean(n):
    n=re.sub(r'\b(Freshly Squeezed|Fresh Squeezed|Fresh|Bitter|100% Agave|100% agave)\b','',n)
    n=re.sub(r'\*','',n); n=re.sub(r'\s+',' ',n).strip()
    n={'Champagne to serve on the side':'Champagne (on the side)','Honey mix (replace water with chamomile)':'Chamomile honey mix','Cream (Chilled)':'Cream','Lime':'Lime juice','Chilled Champagne':'Champagne','Red wine (Shiraz or Malbech)':'Red wine (Shiraz or Malbec)'}.get(n,n)
    return case(n)[0].upper()+case(n)[1:]
PN=['Campari','Cointreau','Kahlúa','Luxardo','Aperol','Chartreuse','Drambuie','Lillet Blanc','Angostura','Peychaud','Grand Marnier','Fernet Branca','Fernet','Cynar','Nonino','Old Tom','London','Cuban','Jamaican','Jamaica','Puerto Rican','Martinique','Demerara','Irish','Goslings','Smirnoff','Havana Club','Lagavulin','Monin','Donn','Bénédictine','DOM','Cinzano Rosso','Italian','Worcestershire','Tabasco','Pernod','Shiraz','Malbec','Frangelico','Prosecco','Champagne','Espadin','Calvados','Sangue Morlacco']
def case(n):
    n=n.lower().replace('gengibre','ginger').replace('  ',' ')
    for p in PN: n=re.sub(re.escape(p.lower()),p,n)
    return n
out=[]
for o in src:
    lines=[]
    for l in o['ing']:
        if l=='Luxardo': continue
        l=l.replace('Maraschino Luxardo','Maraschino')
        if 'Elizabeth15 ml' in l: lines+= ['7.5 ml Allspice dram','15 ml Fresh Lime Juice']; continue
        lines.append(l)
    ings=[];ex=[]
    for l in lines:
        e=next((v for (s,sub),v in EST.items() if s==o['slug'] and sub in l),None)
        if e: ings.append([e[0],e[1],e[2],1]); continue
        m=re.match(r'^(\d+(?:\.\d+)?)\s*(ml)?\s+(.*)$',l)
        if m and (m.group(2) or (o['slug']=='iba-tiki' and 'Fresh' in l)):
            n=clean(m.group(3)); ings.append([n,cls(n),round(float(m.group(1))/10,3)])
        else: ex.append(case(l).replace('’',"'"))
    out.append([o['name'].replace('’',"'").replace('‘',"'"),CAT[o['cat']],"","",ings,ex])
open('iba.js','w').write(',\n'.join(json.dumps(x,ensure_ascii=False) for x in out))
for x in out: print(x[0],'|',' ; '.join(f'{i[0]}[{i[1]}{"~" if len(i)>3 else ""}{i[2]}]' for i in x[4]),'|| +',', '.join(x[5]))
