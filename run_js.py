import subprocess
import json

js_code = """
(function() {
  var result = {};
  
  // 1. Check if openBooking function exists
  result.openBookingExists = (typeof window.openBooking === 'function');
  
  // 2. Check if bookingModal element exists
  var bookingModal = document.getElementById('bookingModal');
  result.bookingModalExists = !!bookingModal;
  if (bookingModal) {
    result.bookingModalDetails = {
      id: bookingModal.id,
      className: bookingModal.className,
      style: bookingModal.getAttribute('style'),
      visible: bookingModal.offsetWidth > 0 && bookingModal.offsetHeight > 0
    };
  }
  
  // Find "Book nå" buttons and look for any Privatkurs association
  var buttons = Array.from(document.querySelectorAll('button, a, div, span'));
  var bookNaButtons = buttons.filter(b => b.textContent && b.textContent.trim().toLowerCase().includes('book nå'));
  
  result.book_na_buttons_found = bookNaButtons.length;
  result.book_na_buttons_details = bookNaButtons.map(b => ({
    tagName: b.tagName,
    className: b.className,
    text: b.textContent.trim(),
    visible: b.offsetWidth > 0 && b.offsetHeight > 0
  }));
  
  // Try to find Privatkurs container
  var containers = Array.from(document.querySelectorAll('*')).filter(el => {
    return el.textContent && el.textContent.includes('Privatkurs');
  });
  
  var clicked = false;
  var clickTargetDetails = null;
  
  // Find Privatkurs element and then its associated "Book nå" button
  for (var b of bookNaButtons) {
    var isVisible = b.offsetWidth > 0 && b.offsetHeight > 0;
    // Walk up the DOM to see if Privatkurs is in the parent chain
    var parent = b.parentElement;
    var isPrivatkurs = false;
    while (parent && parent !== document.body) {
      if (parent.textContent && parent.textContent.includes('Privatkurs')) {
        isPrivatkurs = true;
        break;
      }
      parent = parent.parentElement;
    }
    
    // Also check if the button itself or any sibling has Privatkurs
    if (!isPrivatkurs && b.parentElement) {
      var sibs = Array.from(b.parentElement.children);
      for (var sib of sibs) {
        if (sib.textContent && sib.textContent.includes('Privatkurs')) {
          isPrivatkurs = true;
          break;
        }
      }
    }
    
    if (isPrivatkurs && isVisible) {
      clickTargetDetails = {
        tagName: b.tagName,
        className: b.className,
        text: b.textContent.trim()
      };
      b.click();
      clicked = true;
      break;
    }
  }
  
  // Fallback click if we didn't find with path association but there's a visible one
  if (!clicked && bookNaButtons.length > 0) {
    var visibleButtons = bookNaButtons.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0);
    if (visibleButtons.length > 0) {
      // Let's see if we can identify which one is for Privatkurs by searching text list
      for (var vb of visibleButtons) {
        // Let's see if any header/container near it contains Privatkurs
        clickTargetDetails = {
          tagName: vb.tagName,
          className: vb.className,
          text: vb.textContent.trim()
        };
        vb.click();
        clicked = true;
        break;
      }
    }
  }
  
  result.clicked = clicked;
  result.clickedDetails = clickTargetDetails;
  
  return JSON.stringify(result);
})()
"""

# Escape single quotes and backslashes for AppleScript
escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

applescript = f'tell application "Google Chrome" to execute active tab of window 1 javascript "{escaped_js}"'

proc = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
print("STDOUT:", proc.stdout)
print("STDERR:", proc.stderr)
