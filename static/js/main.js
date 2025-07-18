// Placeholder JS logic
console.log("Bookshelf JS loaded");

// Auto-hide flash messages after 4 seconds
 document.querySelectorAll('.flash-messages li').forEach(msg => {
   setTimeout(() => {
     msg.style.opacity = '0';
     setTimeout(()=> msg.remove(), 700); // remove after fade transition
   }, 1000);
 });