class Profiler {
    constructor() {
    }
}
/*
$(function() {
  var canWrite = true; //this is the default for test purposes

  ge = new GanttMaster();
  ge.set100OnClose=true;

  ge.shrinkParent=true;

  ge.init($("#workSpace"));
  loadI18n(); //overwrite with localized ones

  //in order to force compute the best-fitting zoom level
  delete ge.gantt.zoom;

  var project = resumed_project_data;
  var offset = new Date().getTime() - project.tasks[0].start;
  for (var i=0; i < project.tasks.length;i++) {
    project.tasks[i].start = project.tasks[i].start + offset;
  }
  // var project = getDemoProject();

  if (!project.canWrite)
    $(".ganttButtonBar button.requireWrite").attr("disabled","true");

  ge.loadProject(project);
  ge.checkpoint(); //empty the undo stack

  initializeHistoryManagement(ge.tasks[0].id);
});
*/
/*
function loadI18n() {
  GanttMaster.messages = {
    "CANNOT_WRITE":"No permission to change the following task:",
    "CHANGE_OUT_OF_SCOPE":"Project update not possible as you lack rights for updating a parent project.",
    "START_IS_MILESTONE":"Start date is a milestone.",
    "END_IS_MILESTONE":"End date is a milestone.",
    "TASK_HAS_CONSTRAINTS":"Task has constraints.",
    "GANTT_ERROR_DEPENDS_ON_OPEN_TASK":"Error: there is a dependency on an open task.",
    "GANTT_ERROR_DESCENDANT_OF_CLOSED_TASK":"Error: due to a descendant of a closed task.",
    "TASK_HAS_EXTERNAL_DEPS":"This task has external dependencies.",
    "GANNT_ERROR_LOADING_DATA_TASK_REMOVED":"GANNT_ERROR_LOADING_DATA_TASK_REMOVED",
    "CIRCULAR_REFERENCE":"Circular reference.",
    "CANNOT_DEPENDS_ON_ANCESTORS":"Cannot depend on ancestors.",
    "INVALID_DATE_FORMAT":"The data inserted are invalid for the field format.",
    "GANTT_ERROR_LOADING_DATA_TASK_REMOVED":"An error has occurred while loading the data. A task has been trashed.",
    "CANNOT_CLOSE_TASK_IF_OPEN_ISSUE":"Cannot close a task with open issues",
    "TASK_MOVE_INCONSISTENT_LEVEL":"You cannot exchange tasks of different depth.",
    "CANNOT_MOVE_TASK":"CANNOT_MOVE_TASK",
    "PLEASE_SAVE_PROJECT":"PLEASE_SAVE_PROJECT",
    "GANTT_SEMESTER":"Semester",
    "GANTT_SEMESTER_SHORT":"s.",
    "GANTT_QUARTER":"Quarter",
    "GANTT_QUARTER_SHORT":"q.",
    "GANTT_WEEK":"Week",
    "GANTT_WEEK_SHORT":"w."
  };
}
 */
function saveGanttOnServer() {
    let prj = ge.saveGantt();
    /*
    download(JSON.stringify(prj, null, '\t'), "MyProject.json", "application/json");
    */
    /* var prof = new Profiler("saveServerSide");
    prof.reset(); */
    /*
    if (ge.deletedTaskIds.length>0) {
      if (!confirm("TASK_THAT_WILL_BE_REMOVED\n"+ge.deletedTaskIds.length)) {
        return;
      }
    }
     */
    $.ajax({
        type: 'POST',
        url: '/organization/save/' + project_id,
        data: JSON.stringify(prj),
        contentType: 'application/json',
        success: function (response_data) {
            console.log("Yay");
        }
    });
    /*
    $.ajax("ganttAjaxController.jsp", {
      dataType:"json",
      data: {CM:"SVPROJECT",prj:JSON.stringify(prj)},
      type:"POST",
  
      success: function(response) {
        if (response.ok) {
          prof.stop();
          if (response.project) {
            ge.loadProject(response.project); //must reload as "tmp_" ids are now the good ones
          } else {
            ge.reset();
          }
        } else {
          var errMsg="Errors saving project\n";
          if (response.message) {
            errMsg=errMsg+response.message+"\n";
          }
  
          if (response.errorMessages.length) {
            errMsg += response.errorMessages.join("\n");
          }
  
          alert(errMsg);
        }
      }
    });
   */
}
