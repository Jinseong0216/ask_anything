import Http from "@/api/index"

/*
  수업관련 API 모음
*/
export const lectureApi = {
  lectureRegister(payload) {
    console.log("강의등록 요청")
    return Http.post("/lectures/register", payload)
  },

//   학생 강의 등록 (초대코드 방식)
  enrollLecture(inviteCode) {
    console.log("학생 강의등록 요청")
    return Http.post("/lectures/enroll", {
      invite_code: inviteCode
    })
  },

//   학생 선생 공용api 
  getMyLectures() {
    return Http.get("/lectures/my")
  },
}
