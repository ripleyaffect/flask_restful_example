/* Interaction for projects and project progress */

// Initialize the store for calculating progress
var projectProgressStore = {}

var calculateProgress = function calculateProgress(projectId) {
  console.log(projectProgressStore);
  if (projectProgressStore[projectId]) {
    return Math.min(
      projectProgressStore[projectId].totalProgress /
      projectProgressStore[projectId].goal, 1) * 100
  }
  return 0;
}

var setProgressBar = function setProgressBar(projectId) {
  var value = calculateProgress(projectId);
  var percent = '' + value + '%'
  $('#project-' + projectId + '-progress-fill').width(percent)
}

var projectElementFromObject = function projectElementFromObject(project) {
  return '<div class="project" id="project-' + project.id + '">' +
    '<h3 class="row start-xs">' + project.title + ': ' + project.goal + ' ' +  project.unit + '</h3>' +
    '<div class="row start-xs project-progress-container">' +
      '<div class="col-xs-12 project-progress-bar">' +
        '<div class="project-progress-fill success" id="project-' + project.id + '-progress-fill" style="width: 0%;"></div>' +
      '</div>' +
    '</div>' +
    '<div class="row start-xs">' +
      '<p>' + project.description + '</p>' +
    '</div>' +
    '<div id="project-' + project.id + '-progress-list"/>' +
    '<div class="row">' +
      '<button class="project-delete-button col-xs-3 start-xs danger" onclick="deleteProject(' + project.id + ')">Delete</button>' +
      '<div class="col-xs-9 end-xs between-xs">' +
        '<input class="col-xs-3 project-progress-input" id="project-' + project.id + '-progress-input" type="number" value="1">' + 
        '<button class="success-button project-progress-submit-button" onclick="submitNewProjectProgress(' + project.id + ')">Add time</button>' +
      '</div>' +
    '</div>' +
  '</div>'
};


var projectProgressFromObject = function projectProgressFromObject(progress) {
  return '<div id="project-progress-' + progress.id + '" class="project-progress-container row">' +
    '<div class="project-progress col-xs-12">' +
      '<div class="row">' +
        '<button onclick="deleteProgress(' +
            progress.project_id + ', ' +
            progress.id +', ' +
            progress.value + ')" class="progress-delete-button danger col-xs-1">' +
          '&times;' +
        '</button>' +
        '<div class="project-progress-message col-xs-11">' +
          progress.value + ' hour' +
          (progress.value === 1 ? '' : 's') + ' on ' +
          moment(progress.created_asof).format('dddd, MMMM Do [at] h:mm:ss a') +
        '</div>' +
      '</div>' +
    '</div>' +
  '</div>'
}

var addProjects = function addProjects(projects) {
  var projectsList = $('#projects-list');
  projects.map(function (project) {
    projectsList.prepend(projectElementFromObject(project));
    projectProgressStore[project.id] = {goal: project.goal, totalProgress: 0}
    addProgress(project.id, project.progress);
    setProgressBar(project.id);
  })
};


var addProgress = function addProgress(projectId, progressList) {
  var projectProgressList = $('#project-' + projectId + '-progress-list');
  progressList.map(function (progress) {
    projectProgressList.append(projectProgressFromObject(progress));
    projectProgressStore[projectId].totalProgress += progress.value;
  })
};


var removeProject = function removeProject(projectId) {
  $('#project-' + projectId).remove();
  delete projectProgressStore[projectId];
}

var removeProgress = function removeProgress(projectId, progressId, value) {
  $('#project-progress-' + progressId).remove();
  projectProgressStore[projectId].totalProgress -= value;
  setProgressBar(projectId);
}


var deleteProject = function deleteProject(projectId) {
  if (confirm('Are you sure you want to remove this project?')) {
    $.ajax({
      type: 'DELETE',
      url: '/api/projects/' + projectId,
      success: function(data, status, response) {
        response.status === 204 ? removeProject(projectId) : console.log(data)
      }
    });
  }
  $('.project-delete-button').blur();
};


var deleteProgress = function deleteProgress(projectId, progressId, value) {
  if (confirm('Are you sure you want to remove this progress?')) {
    $.ajax({
      type: 'DELETE',
      url: '/api/projects/' + projectId + '/progress/' + progressId,
      success: function(data, status, response) {
        response.status === 204 ?
          removeProgress(projectId, progressId, value) : console.log(data)
      }
    });
  }
  $('.progress-delete-button').blur();
};


var clearProjectFields = function clearProjectFields() {
  $("#new-project-title")[0].value = ''
  $("#new-project-goal")[0].value = 10;
  $("#new-project-description")[0].value = ''
}


var validateNewProject = function validateNewProject (project) {
  var newProjectTitle = $("#new-project-title")
  var newProjectGoal = $("#new-project-goal")
  var newProjectDescription = $("#new-project-description")

  // clear error classes 
  newProjectTitle.removeClass('error')
  newProjectGoal.removeClass('error')
  newProjectDescription.removeClass('error')
  var fieldNodes = {
    title: newProjectTitle,
    goal: newProjectGoal,
    description: newProjectDescription
  }

  // All fields are required
  var valid = true;
  ['title', 'goal', 'description'].map(function (field) {
    if (!project[field]) {
      valid = false
      fieldNodes[field].addClass('error')
    }
  });

  // Cannot have a negative number
  if (project.goal <= 0) {
    valid = false;
    fieldNodes.goal.addClass('error')
  }

  return valid;
}


var submitNewProject = function submitNewProject(event) {
  event.preventDefault();

  var button = $('#new-project-button').blur();

  var newProjectTitle = $("#new-project-title")[0].value
  var newProjectGoal = $("#new-project-goal")[0].value
  var newProjectDescription = $("#new-project-description")[0].value
  var newProjectUnit = 'hours'
  var data = {
    title: newProjectTitle,
    goal: newProjectGoal,
    description: newProjectDescription,
    unit: newProjectUnit
  }
  if (validateNewProject(data)) {
    $.ajax({
      type: 'POST',
      url: '/api/projects',
      data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      success: function(data, status, response) {
        if (response.status === 201) {
          addProjects(data);
          clearProjectFields();
        }
        else {
          console.log('There was a problem creating a new project:');
          console.log(data);
        }
      },
      dataType: 'json'});
  }
};

var submitNewProjectProgress = function submitNewProjectProgress(projectId) {
  console.log(projectId);
  var newProgressValue = $('#project-' + projectId + '-progress-input')[0].value
  var data = { value: newProgressValue };
  $.ajax({
      type: 'POST',
      url: '/api/projects/' + projectId + '/progress',
      data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      success: function(data, status, response) {
        if (response.status === 201) {
          addProgress(projectId, data);
          setProgressBar(projectId);
        }
        else {
          console.log('There was a problem creating a new project:');
          console.log(data);
        }
      },
      dataType: 'json'});
  $('.project-progress-submit-button').blur()
}

$(document).ready(function () {
  $.get('/api/projects', function (data) {
    addProjects(data)
  })

  $("#new-project-form").submit(submitNewProject);
});
