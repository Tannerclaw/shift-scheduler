// Simple WhatsApp sender - paste this in browser console
function sendToWhatsApp(){
  const date=new Date().toLocaleDateString(undefined,{weekday:'long',month:'short',day:'numeric'});
  let msg='*Shift Schedule - ' + date + '*\n\n';
  
  // Get from localStorage
  const data=JSON.parse(localStorage.getItem('shiftV4')||'{}');
  const workers=data.workers||[];
  const assignments=data.assignments||{};
  
  for(const time in assignments){
    const names=assignments[time];
    if(names.length>0){
      msg+='*' + time + '*\n';
      msg+='Workers: ' + names.join(', ') + '\n\n';
    }
  }
  
  msg+='Sent from Shift Scheduler';
  
  // Open WhatsApp
  window.open('https://wa.me/?text=' + encodeURIComponent(msg),'_blank');
}

// Run it
sendToWhatsApp();
