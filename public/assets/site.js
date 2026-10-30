// Japanese Grimoire – nav toggle and newsletter opt-in (Brevo)
(function(){
  var t=document.querySelector('.nav-toggle'),l=document.getElementById('nav-links');
  if(t&&l){t.addEventListener('click',function(){var o=l.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});}
  var ENDPOINT='https://dc276ca0.sibforms.com/serve/MUIFAK3fpJiNFfswdNu2AO5M-RKM1x3FtAWlQZ8fPDXdvGkHoPCiDKbq4X0UmKs6Diz5qE2Gdrkg_vWOYPxgxlvu9Ubd4Vv_lLKNcQEIOBzfN9GgG_UKBUpnVld2k5wvCnIxeJcKPe7LwB6ioMHB8KujB_rg8eiECf-sAEFm8Zp2XSzS8m36istfPoVL69fCpmgT6m_igc1yxSxyBg==?isAjax=1';
  document.querySelectorAll('form.optin-form').forEach(function(form){
    var btn=form.querySelector('button'),status=form.querySelector('.form-status'),email=form.querySelector('input[type=email]'),orig=btn.innerHTML;
    function set(m,k){status.textContent=m||'';status.className='form-status'+(k?' is-'+k:'');}
    form.addEventListener('submit',function(ev){
      ev.preventDefault();set('','');
      var v=(email.value||'').trim();
      if(!v||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)){set('Please enter a valid email address.','error');email.focus();return;}
      btn.disabled=true;btn.innerHTML='Sending...';
      var fd=new FormData();fd.append('EMAIL',v);fd.append('email_address_check','');fd.append('locale','en');
      fetch(ENDPOINT,{method:'POST',body:fd,headers:{'Accept':'application/json'}}).then(function(res){
        return res.json().catch(function(){return {};}).then(function(d){
          if(res.ok){window.location.href='/thank-you.html';return;}
          set((d&&d.error)||'Something went wrong. Please try again.','error');
        });
      }).catch(function(){set('Network problem. Please try again.','error');}).then(function(){btn.disabled=false;btn.innerHTML=orig;});
    });
  });
})();
