"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Profiler = /** @class */ (function () {
    function Profiler() {
    }
    return Profiler;
}());
function saveGanttOnServer() {
    var a = 1;
    //this is a simulation: save data to the local storage or to the textarea
    //saveInLocalStorage();
    /*
    var prj: GanttMaster = ge.saveProject();
  
    /*
    download(JSON.stringify(prj, null, '\t'), "MyProject.json", "application/json");
    */
    /*
      delete prj.resources;
      delete prj.roles;
    
      /* var prof = new Profiler("saveServerSide");
      prof.reset(); */
    /*
      if (ge.deletedTaskIds.length>0) {
        if (!confirm("TASK_THAT_WILL_BE_REMOVED\n"+ge.deletedTaskIds.length)) {
          return;
        }
      }
    
      $.ajax({
          type: 'POST',
          url: '/organization/save',
          data: JSON.stringify(prj),
          contentType: 'application/json',
          success: function (response_data) {
              console.log("Yay");
          }
      });
    
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
//# sourceMappingURL=main.js.map