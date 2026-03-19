// Parse vCard file and extract contacts
function parseVCard(vcardText){
  const contacts=[];
  const cards=vcardText.split('BEGIN:VCARD');
  
  cards.forEach(card=>{
    if(!card.includes('END:VCARD'))return;
    
    const nameMatch=card.match(/FN:(.+?)(?:\r?\n|$)/);
    const telMatch=card.match(/TEL[^:]*:(.+?)(?:\r?\n|$)/);
    
    if(nameMatch){
      const name=nameMatch[1].trim();
      const phone=telMatch?telMatch[1].replace(/[^0-9+]/g,''):'';
      
      // Skip if it's Dan (you)
      if(name.toLowerCase().includes('dan')&&name.toLowerCase().includes('richards'))return;
      
      contacts.push({name,phone});
    }
  });
  
  return contacts;
}

// Import contacts from vCard file
function importContactsFromVCard(vcardText){
  const contacts=parseVCard(vcardText);
  let added=0;
  let skipped=0;
  
  contacts.forEach(contact=>{
    // Check if already exists
    if(!st.workers.find(w=>w.name===contact.name)){
      st.workers.push({
        name:contact.name,
        phone:contact.phone,
        unavailable:false
      });
      added++;
    }else{
      skipped++;
    }
  });
  
  save();
  render();
  
  return{added,skipped,total:contacts.length};
}
