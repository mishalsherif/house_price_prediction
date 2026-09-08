async function getMetadata(){
  const res = await fetch('/metadata');
  return res.json();
}

function clearChildren(el){while(el.firstChild)el.removeChild(el.firstChild)}

function formatSelectOptions(select, items){
  clearChildren(select);
  const opt = document.createElement('option'); opt.textContent = 'Select'; opt.value=''; select.appendChild(opt);
  for(const it of items){
    const o = document.createElement('option'); o.value = it; o.textContent = it; select.appendChild(o);
  }
}

async function init(){
  const metaResp = await getMetadata();
  if(!metaResp.success){
    alert('Metadata not found. Train the model first.');
    return;
  }
  const md = metaResp.metadata;
  const districtSelect = document.getElementById('district');
  const localitySelect = document.getElementById('locality');
  const areaTypeInput = document.getElementById('area_type');
  const propertyType = document.getElementById('property_type');
  const furnishing = document.getElementById('Furnishing');
  const roadAccess = document.getElementById('Road_Access');

  const districts = Object.keys(md.district_localities || {}).sort();
  formatSelectOptions(districtSelect, districts);
  formatSelectOptions(areaTypeInput, md.Area_Type || []);
  formatSelectOptions(propertyType, md.Property_Type || []);
  formatSelectOptions(furnishing, md.Furnishing || []);
  formatSelectOptions(roadAccess, md.Road_Access || []);

  districtSelect.addEventListener('change', ()=>{
    const d = districtSelect.value;
    const localities = md.district_localities[d] || [];
    formatSelectOptions(localitySelect, localities);
    // auto-select first valid locality
    if(localities.length>0){ localitySelect.selectedIndex = 1; localeChanged(); }
  });

  function localeChanged(){
    const loc = localitySelect.value;
    const at = md.locality_area_type && md.locality_area_type[loc];
    if(at) {
      areaTypeInput.value = at;
    } else {
      // keep previously selected or set to default
      if(areaTypeInput.options && areaTypeInput.options.length>0) areaTypeInput.selectedIndex = 0;
    }
  }

  localitySelect.addEventListener('change', localeChanged);

  document.getElementById('predict-btn').addEventListener('click', async ()=>{
    const payload = {
      District: districtSelect.value,
      Locality: localitySelect.value,
    Area_Type: areaTypeInput.value,
      Property_Type: propertyType.value,
      Area_sqft: Number(document.getElementById('area_sqft').value),
      BHK: Number(document.getElementById('BHK').value),
      Bathrooms: Number(document.getElementById('Bathrooms').value),
      Property_Age_Years: Number(document.getElementById('Property_Age_Years').value),
      Parking_Spaces: Number(document.getElementById('Parking_Spaces').value),
      Furnishing: furnishing.value,
      Floor: Number(document.getElementById('Floor').value),
      Distance_to_City_Center_km: Number(document.getElementById('Distance_to_City_Center_km').value),
      Road_Access: roadAccess.value,
      Gated_Community: document.getElementById('Gated_Community').value,
    };

    // Basic client validation
    if(!payload.District || !payload.Locality){ alert('Please select District and Locality'); return; }
    if(!payload.Area_sqft || payload.Area_sqft<=0){ alert('Area must be > 0'); return; }
    if(!payload.BHK || payload.BHK<1){ alert('BHK must be >=1'); return; }
    if(!payload.Bathrooms || payload.Bathrooms<1){ alert('Bathrooms must be >=1'); return; }

    const res = await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const data = await res.json();
    if(!data.success){ alert(data.error || 'Prediction failed'); return; }

    document.getElementById('result-amount').textContent = data.formatted;
    document.getElementById('result-note').textContent = '';
    document.getElementById('model-name').textContent = 'Model: ' + (data.model||'Ridge Regression');
    document.getElementById('model-r2').textContent = 'R²: ' + (data.r2!==undefined?data.r2.toFixed(3):'—');
  });
}

window.addEventListener('DOMContentLoaded', init);
