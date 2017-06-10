var ServerRequest = function(method, path, data, callback) {
  var request = new XMLHttpRequest();
  request.open(method, path);
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if (request.readyState === 4) {
      return callback(JSON.parse(request.responseText))
    }
  };

  return request.send(JSON.stringify(data));
};

var sendDecide = function(item) {
  value = item.getAttribute('data-value');
  while ((item = item.parentElement) && !item.classList.contains('line'));
  id = item.getAttribute('data-id');

  ServerRequest('get', '/decide/' + id + '/' + value, {}, function(data) {
    newitem = renderOneLine(data['prop'])
    item.innerHTML = newitem.innerHTML;
    item.className = newitem.className;
  });
};

var templates = {
  line: `<div class="title">
    {location_path}
    <a href="https://ingatlan.com/{id}" target="_blank">open</a>
    <span>{price_note}{price} HUF / mo</span>
  </div>
  <div class="rooms">
    <span class="label">Area: <span class="value">{area}</span></span>
    <span class="label">Rooms: <span class="value">{number_of_rooms}</span></span>
  </div>
  <div class="left">
    <div class="properties">{property_list}</div>
  </div>
  <div class="right">
    <div class="decide-buttons">
      <button onclick="sendDecide(this);" data-value="1">✔</button><button onclick="sendDecide(this)" data-value="-1">✘</button>
    </div>
    <div class="prediction">Prediction: <span>{prediction_value}</span></div>
  </div>`,
  property_row: `<span class="label">{title}: <span class="value">{value}</span></span>`
}

var evaluateTemplate = function(template, data) {
  for (key in data) {
    template = template.replace('{' + key + '}', data[key]);
  }
  return template;
};

var yesNoString = function(value) {
  return (value == 1 ? "Yes" : "No");
};

var renderOneLine = function(p) {
  var line = document.createElement('div');
  line.className = 'line';
  if (p[13] == -1) {
    line.className += ' decided-no';
  }
  if (p[13] == 1) {
    line.className += " decided-yes";
  }
  line.setAttribute("data-id", p[0]);
  rooms = "" + p[7];
  if (p[8] > 0) {
    rooms += " + " + p[8] + " <span class='note'>(half room)</span>";
  }
  predicted_value = "unknown";
  if (p[12] > 0) {
    predicted_value = "✔";
  } else if (p[12] < 0) {
    predicted_value = "✘";
  }

  properties = [
    evaluateTemplate(templates['property_row'], {title: "Elevator", value: p[3]}),
    evaluateTemplate(templates['property_row'], {title: "Appliances", value: p[5]}),
    evaluateTemplate(templates['property_row'], {title: "Furnished", value: p[6]}),
    evaluateTemplate(templates['property_row'], {title: "AreaUnit", value: Math.round(p[2]/p[1]) + " huf/m2"})
  ]

  line.innerHTML = evaluateTemplate(templates['line'], {
    id: p[0],
    area: p[1],
    price: p[2] + Math.max(0, p[4]),
    price_note: (p[4] > 0 ? "<em>(with utility cost)</em> " : ""),
    number_of_rooms: rooms,
    location_path: p[9],
    prediction_value: predicted_value,
    property_list: properties.join("")
  });

  if (p[13] != 0) {
    line.querySelector('.decide-buttons').innerHTML = "<span class='decided'>" + yesNoString(p[13]) + "</span>"
  }

  return line;
};

var render = function(props) {
  var lines = props.map(renderOneLine);

  lines.forEach(function(p) { ROOT.appendChild(p); });
};

var ROOT = document.querySelector(".container");
ROOT.innerHTML = '';

ServerRequest('get', '/properties', {}, function(data) {
  var properties = data['properties'];
  render(properties);
});
