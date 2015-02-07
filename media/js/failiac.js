'use strict';
var Failiac = (function () {
	var r = {
			professionHTML: '<h3 id="profession-{{ professionId }}">{{ professionName }}</h3>' +
			'<div class="data" id="data-{{ professionId }}">' +
				'<dl>' +
					'<dd class="count">People Count</dd>' +
					'<dt class="count"></dt>' +
					'<dd class="min">Minimum percentage</dd>' +
					'<dt class="min"></dt>' +
					'<dd class="max">Maximum percentage</dd>' +
					'<dt class="max"></dt>' +
					'<dd class="range">Range (max - min)</dd>' +
					'<dt class="range"></dt>' +
					'<dd class="average">Average</dd>' +
					'<dt class="average"></dt>' +
					'<dd class="mean">Mean</dd>' +
					'<dt class="mean"></dt>' +
					'<dd class="median">Median</dd>' +
					'<dt class="median"></dt>' +
					'<dd class="std">Standard Deviation</dd>' +
					'<dt class="std"></dt>' +
					'<dd class="superimpose"><a href="#" class="superimpose-all">Superimpose "All"</a>' +
					'<dt class="superimpose"></dt>' +
					'<dd class="superimpose"><a href="#" class="superimpose-birthed">Superimpose "Birthed"</a></dd>' +
					'<dt class="superimpose"></dt>' +
				'</dl>' +
				'<div id="{{ professionSlug }}" class="chart"></div>' +
			'</div>',
			slugValidChars: /[^a-z0-9 -]/g,
			whitespaces: /\s+/g,
			multiDashes: /-+/g,
			percentageFormatter: {},
			percentagePointsFormatter: {},
			drawCollapsible: function (h3, fillData) {
				var superimpose = [];

				$.each(h3.data('superimpose') || [], function (i, profession) {
					superimpose.push(u.superimpose(profession));
				});

				u.drawChart(h3.text(), superimpose);
				if (fillData) {
					u.fillData(h3.text());
				}
				h3.data('loaded', true);
			},
			initSorting: function () {
				var sorting = $('#sorting');

				sorting.on('click', '.members', function (ev) {
					var a = $(this);

					ev.preventDefault();
					r.sortByList(FailiacZodiacs.byMembers, a);
				}).on('click', '.range', function (ev) {
					var a = $(this);

					ev.preventDefault();
					r.sortByList(FailiacZodiacs.byRange, a);
				}).on('click', '.standard-deviation', function (ev) {
					var a = $(this);

					ev.preventDefault();
					r.sortByList(FailiacZodiacs.byStandardDeviation, a);
				});
			},
			sortByList: function (sortedList, a) {
				var professions = $('#professions'),
					span = a.next();

				if (span.prop('class').indexOf('asc') >= 0) {
					span.prop('class', span.prop('class').replace('asc', 'desc'));
				} else {
					span.prop('class', span.prop('class').replace('desc', 'asc'));
				}
				sortedList.reverse();
				$.each(sortedList, function (i, profession) {
					var title = $('#profession-' + u.slugify(profession)),
						data = $('#data-' + u.slugify(profession));

					title.detach();
					data.detach();

					professions.append(title).append(data);
				});
			},
			onFactsPage: function () {
				var professions = $('#professions');

				$('form').on('submit', function (ev) {ev.preventDefault()}); // Kill the forms
				$('#profession-all').data('superimpose', ['Birthed']);
				$('#pop-count').text(FailiacZodiacs.zodiacs.All.members);
				u.drawChart('Birthed');
				u.fillData('Birthed');
				u.drawChart('All', [u.superimpose('Birthed')]);
				u.fillData('All');
				u.drawChart('Simulated Earth Population', [u.superimpose('All')]);
				u.fillData('Simulated Earth Population');
				u.drawStdVsMembers('std-vs-members');

				r.initFilter();
				r.initCalculator();
				r.initSorting();

				$.each(FailiacZodiacs.names, function (i, profession) {
					professions.append(r.professionHTML.replace('{{ professionId }}', u.slugify(profession)).replace('{{ professionId }}', u.slugify(profession)).replace('{{ professionName }}', profession).replace('{{ professionSlug }}', u.slugify(profession)));
				});
				professions.find('.data').hide();
				professions.on('click', 'h3', function (ev) {
					var h3 = $(this);
					h3.next().toggle();
					if (!h3.data('loaded')) {
						r.drawCollapsible(h3, true);
					}
				});
				professions.on('click', '.superimpose-all', function (ev) {
					var h3 = $(this).closest('.data').prev(),
						superimpose = h3.data('superimpose');

					ev.preventDefault();

					if (!superimpose) {
						h3.data('superimpose', ['All']);
					} else {
						if (superimpose.indexOf('All') === -1) {
							superimpose.push('All');
							h3.data('superimpose', superimpose);
						} else {
							superimpose.splice(superimpose.indexOf('All'), 1);
							h3.data('superimpose', superimpose);
						}
					}
					r.drawCollapsible(h3);
				});
				professions.on('click', '.superimpose-birthed', function (ev) {
					var h3 = $(this).closest('.data').prev(),
						superimpose = h3.data('superimpose');

					ev.preventDefault();

					if (!superimpose) {
						h3.data('superimpose', ['Birthed']);
					} else {
						if (superimpose.indexOf('Birthed') === -1) {
							superimpose.push('Birthed');
							h3.data('superimpose', superimpose);
						} else {
							superimpose.splice(superimpose.indexOf('Birthed'), 1);
							h3.data('superimpose', superimpose);
						}
					}
					r.drawCollapsible(h3);
				});
			},
			initCalculator: function () {
				$('#calculator').on('input', '#birthday', function (ev) {
					var date = $(this).val(),
						month = parseInt(date.split('-')[1], 10),
						day = parseInt(date.split('-')[2], 10);

					console.log([day, month]);
				});
				if ($('#birthday').prop('type') !== 'date') {
					$('#birthday').prop('placeholder', 'Must be format YYYY-MM-DD');
				}
			},
			initFilter: function () {
				var index = {},
					professions = $('#professions');

				$.each(FailiacZodiacs.names, function (i, profession) {
					index[profession.toLowerCase()] = u.slugify(profession);
				});

				$('#filter').on('input', function(ev) {
					var filter = $(this).val() || '';

					filter = filter.toLowerCase();

					if ($.trim(filter) === '') {
						professions.find('h3').show();
					}

					$.each(index, function (indexed, id) {
						var graph = $('#' + id);

						if (indexed.indexOf(filter) > -1) {
							graph.closest('.data').prev().show();
						} else {
							graph.closest('.data').prev().hide();
							graph.closest('.data').hide();
						}
					});
				});
			}
		},
		u = {
			prettyPercents: function (num) {
				return (num * 100.0).toFixed(4) + '%'
			},
			slugify: function (str) {
				return $.trim(str.toLowerCase().replace(r.slugValidChars, '') // remove invalid chars
					.replace(r.whitespaces, '-') // collapse whitespace and replace by -
					.replace(r.multiDashes, '-')); // collapse dashes);
			},
			superimpose: function (profession) {
				return function (data) {
					$.each(data, function (i, row) {
						if (i === 0) {
							row.push(profession); // First row, push profession as title
						} else {
							row.push(FailiacZodiacs.zodiacs[profession].distributionPercentages[row[0]]); // Later row, push right sign value
						}
					});
				}
			},
			fillData: function (profession) {
				var definitionList = $('#' + u.slugify(profession)).closest('.data').find('dl');

				definitionList.find('dt.count').text(FailiacZodiacs.zodiacs[profession].members);
				definitionList.find('dt.min').text(u.prettyPercents(FailiacZodiacs.zodiacs[profession].min));
				definitionList.find('dt.max').text(u.prettyPercents(FailiacZodiacs.zodiacs[profession].max));
				definitionList.find('dt.range').empty().append((FailiacZodiacs.zodiacs[profession].range * 100.0).toFixed(4) + '<abbr title="Percentage Points">pp</abbr>');
				definitionList.find('dt.average').text(u.prettyPercents(FailiacZodiacs.zodiacs[profession].average));
				definitionList.find('dt.mean').text(u.prettyPercents(FailiacZodiacs.zodiacs[profession].mean));
				definitionList.find('dt.median').text(u.prettyPercents(FailiacZodiacs.zodiacs[profession].median));
				definitionList.find('dt.std').empty().append((FailiacZodiacs.zodiacs[profession].standardDeviation * 100.0).toFixed(4) + '<abbr title="Percentage Points">pp</abbr>');
			},
			drawChart: function (profession, superimpose, width, height) {
				var win = $(window),
					blob = FailiacZodiacs.zodiacs[profession],
					data = [['Sign', 'Chances']],
					options = {},
					chart = null,
					columns = 0,
					slug = u.slugify(profession),
					i = 1; // Start with second column (later)

				width = width || 900;
				height = height || 400;

				if (win.width() <= 980) {
					width = $('#data-' + slug).width();
				}

				options = {
					width: width,
					height: height,
					vAxis: {
						titleTextStyle: {
							color: '#6633cc'
						},
						minValue: 0,
						format:'#%'
					},
					hAxis: {
						textPosition: 'in'
					},
					sliceVisibilityThreshold:0
				};

				superimpose = superimpose || []; // Default if none are provided

				$.each(FailiacZodiacs.order, function (i, sign) {
					data.push([sign, blob.distributionPercentages[sign]]);
				});
				// Now we superimpose other professions
				$.each(superimpose, function (i, callback) {
					callback(data);
				});

				data = google.visualization.arrayToDataTable(data);

				columns = data.getNumberOfColumns();
				for (; i < columns; i += 1) {
					r.percentageFormatter.format(data, i);
				}

				chart = new google.visualization.LineChart(document.getElementById(slug));
				chart.draw(data, options);
			},
			drawStdVsMembers: function (id, width, height) {
				var win = $(window),
					stdVsCountData = [['Members', 'Percentage', {type: 'string', role: 'tooltip'}]],
					chart = null;

				$.each(FailiacZodiacs.zodiacs, function (profession, blob) {
					stdVsCountData.push([blob.members, blob.standardDeviation * 100.0, profession + ' (members: ' + blob.members + '/standard deviation: ' + (blob.standardDeviation * 100.0).toFixed(4) + 'pp)']);
				});

				stdVsCountData = google.visualization.arrayToDataTable(stdVsCountData);
				r.percentagePointsFormatter.format(stdVsCountData, 1);

				width = width || 1175;
				height = height || 400;

				if (win.width() <= 980) {
					width = $('#data-data-std-vs-members').width();
				}

				chart = new google.visualization.ScatterChart(document.getElementById(id));
				chart.draw(stdVsCountData, {
					width: width,
					height: height,
					pointSize: 2,
					vAxis: {
						title: 'Standard Deviation',
						minValue: 0
					},
					hAxis: {
						title: 'Members',
						logScale: true
					},
					sliceVisibilityThreshold:0
//					,
//					trendlines: {0: {}} // Literally waiting on Google to release the fix for this one :) https://code.google.com/p/google-visualization-api-issues/issues/detail?id=1820&q=log%20scale&colspec=ID%20Stars%20Modified%20Type%20Status%20Priority%20Milestone%20Owner%20Summary
				});

				google.visualization.events.addListener(chart, 'select', function () {
					var selectedItem = chart.getSelection()[0];
						id = '';
					if (selectedItem) {
						id = '#profession-' + u.slugify(stdVsCountData.getValue(selectedItem.row, 2).split(' (')[0]);
						window.location.href = id;
						if (!$(id).data('loaded')) {
							r.drawCollapsible($(id), true);
						}
						$(id).next().show();
					}
				});
			},
			initialize: function () {
				r.percentageFormatter = new google.visualization.NumberFormat({pattern: '#,###.0000%'});
				r.percentagePointsFormatter = new google.visualization.NumberFormat({pattern: '#,###.0000pp'});
				if ($('body').data('page') === 'facts') { // Treat this page differently
					r.onFactsPage();
				}
			}
		};

	return u;
}());

$(function () {
	google.load('visualization', '1', {
		packages: ['corechart'],
		callback: Failiac.initialize
	});
});