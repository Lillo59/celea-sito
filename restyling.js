/* Restyling 2026-11 · animazioni leggere del sito (nessuna libreria esterna).
   Regole seguite (guida Stageshow): ogni scena racconta una cosa sola, 3-5 passaggi e un risultato che resta
   sullo schermo; il fotogramma di partenza senza JavaScript (o con «riduci movimento») è già il risultato finale.
   Le scene girano solo quando sono visibili e si fermano fuori schermo, per non consumare batteria sul telefono. */
window.CELEA_R_OK=true;
(function(){
  "use strict";
  var doc=document.documentElement;
  var reduce=window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(!("IntersectionObserver" in window)) return;
  doc.classList.add("js-r");

  // 1) Ingressi delle sezioni
  var rev=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); rev.unobserve(e.target); } }); },{rootMargin:"0px 0px -8% 0px"});
  document.querySelectorAll("[data-reveal]").forEach(function(el){ rev.observe(el); });

  // 2) Scene a passaggi: gli elementi data-at="N" compaiono quando la scena arriva al passaggio N
  function Scene(root, beats, onStep){
    this.root=root; this.beats=beats; this.onStep=onStep||function(){}; this.i=0; this.t=null; this.vis=false;
    this.items=[].slice.call(root.querySelectorAll("[data-at]"));
  }
  Scene.prototype.show=function(n){
    this.items.forEach(function(el){ el.classList.toggle("on", +el.dataset.at<=n); });
    this.onStep(n);
  };
  Scene.prototype.next=function(){
    var self=this; if(!self.vis) return;
    var b=self.beats[self.i]; self.show(b[0]);
    self.i=(self.i+1)%self.beats.length;
    self.t=setTimeout(function(){ self.next(); }, b[1]);
  };
  Scene.prototype.start=function(){ if(this.vis) return; this.vis=true; this.root.classList.add("playing"); this.next(); };
  Scene.prototype.stop=function(){ this.vis=false; clearTimeout(this.t); };
  var scenes=[];
  function watch(sel, beats, onStep){
    var root=document.querySelector(sel); if(!root) return;
    var sc=new Scene(root, beats, onStep); scenes.push(sc);
    if(reduce) return; // resta il fotogramma finale
    new IntersectionObserver(function(es){ es.forEach(function(e){ e.isIntersecting ? sc.start() : sc.stop(); }); },{threshold:.35}).observe(root);
  }

  // Telefonata: [passaggio, durata in ms]. 0 squilla, 1-5 la conversazione, 6 l'appuntamento nel calendario, 7 il promemoria.
  var timer=document.querySelector("[data-timer]"), secs=0, tick=null;
  function clock(on, reset){
    if(!timer) return; if(reset){ secs=0; timer.textContent="00:00"; }
    clearInterval(tick); if(on) tick=setInterval(function(){ secs++; timer.textContent="00:"+String(secs).padStart(2,"0"); }, 1000);
  }
  watch("[data-scene=call]", [[0,1200],[1,2300],[2,1800],[3,2600],[4,1600],[5,1500],[6,2600],[7,4200]], function(n){
    if(n===0) clock(false,true); else if(n<6) clock(true); else clock(false);
  });

  // Portale: 0 il cruscotto com'era, 1 arriva la telefonata e i contatori salgono, 2 compare chi richiamare.
  var kpis=[].slice.call(document.querySelectorAll("[data-kpi]"));
  watch("[data-scene=portale]", [[0,1800],[1,2200],[2,5200]], function(n){
    kpis.forEach(function(k,i){ setTimeout(function(){ k.classList.toggle("up", n>=1); }, n>=1 ? 250+i*180 : 0); });
  });

  // 3) Reparti al lavoro: ogni reparto mostra a turno cosa sta facendo (solo quando l'ufficio è visibile)
  var stati=[].slice.call(document.querySelectorAll(".stato")), rt=null;
  function giro(){
    stati.forEach(function(st, k){
      setTimeout(function(){
        var sp=st.querySelectorAll("span"); if(sp.length<2) return;
        var i=[].findIndex.call(sp,function(s){ return s.classList.contains("on"); });
        sp[i<0?0:i].classList.remove("on"); sp[((i<0?0:i)+1)%sp.length].classList.add("on");
      }, k*420);
    });
  }
  var uff=document.querySelector(".palazzo");
  if(uff && !reduce) new IntersectionObserver(function(es){ es.forEach(function(e){ clearInterval(rt); if(e.isIntersecting) rt=setInterval(giro, 3600); }); },{threshold:.25}).observe(uff);

  // 4) «Parla ora» sempre a portata di mano: porta al riquadro «Parli a voce» e avvia la chiamata dal browser.
  var fab=document.getElementById("parla-fab"), talk=document.getElementById("talk"), talkBtn=document.getElementById("talk-btn");
  if(fab){
    var vicino=false, aperto=false;
    function aggiorna(){ fab.classList.toggle("via", vicino || aperto); }
    if(talk) new IntersectionObserver(function(es){ es.forEach(function(e){ vicino=e.isIntersecting; aggiorna(); }); },{threshold:.2}).observe(talk);
    fab.addEventListener("click", function(ev){
      if(!talk || talk.hidden || !talkBtn){ fab.setAttribute("href","#demo"); return; } // senza voce: porta alla demo
      ev.preventDefault();
      talk.scrollIntoView({behavior: reduce ? "auto" : "smooth", block:"center"});
      talkBtn.click();
      aperto=true; aggiorna(); // da qui il pulsante della voce lo mostra il riquadro della chiamata
    });
  }
})();
