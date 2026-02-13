<template>
  <footer class="bg-[#111827] text-neutral-400">
    <div class="max-w-7xl mx-auto px-6 py-7">

      <!-- 상단 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">

        <!-- 회사 정보 -->
        <div class="space-y-1 text-[11px] leading-relaxed text-left">
          <p class="text-white text-sm font-semibold tracking-wide">
            네오매스 에듀테크
          </p>
          <div class="h-px w-8 bg-indigo-400/70"></div>

          <p>NEOMATH EDUTECH Inc.</p>
          <p>대표이사 최낙성</p>
          <p>사업자등록번호 214-87-39216</p>
          <p>통신판매업신고 제2026-서울강남-04123호</p>
          <p>서울특별시 강남구 테헤란로 312, 8층</p>
          <p class="text-neutral-300">
            02-538-2378 · pnum2378@naver.com
          </p>
        </div>

        <!-- 서비스 -->
        <div>
          <h4 class="text-white text-sm font-semibold mb-3 tracking-wide">
            서비스
          </h4>
          <ul class="space-y-1 text-[11px]">
            <li><a class="hover:text-white transition-colors">질문 게시판</a></li>
            <li><a class="hover:text-white transition-colors">학습 관리</a></li>
            <li><a class="hover:text-white transition-colors">학생 리포트</a></li>
            <li><a class="hover:text-white transition-colors">교사용 대시보드</a></li>
            <li><a class="hover:text-white transition-colors">학습 통계</a></li>
          </ul>
        </div>

        <!-- 고객지원 -->
        <div>
          <h4 class="text-white text-sm font-semibold mb-3 tracking-wide">
            고객지원
          </h4>
          <ul class="space-y-1 text-[11px]">
            <li><a class="hover:text-white transition-colors">공지사항</a></li>
            <li><a class="hover:text-white transition-colors">자주 묻는 질문</a></li>
            <li><a class="hover:text-white transition-colors">문의하기</a></li>
            <li><a class="hover:text-white transition-colors">광고 · 제휴 문의</a></li>
            <li><a class="hover:text-white transition-colors">업데이트 내역</a></li>
          </ul>
        </div>

        <!-- 정책 -->
        <div>
          <h4 class="text-white text-sm font-semibold mb-3 tracking-wide">
            정책
          </h4>
          <ul class="space-y-1 text-[11px]">
            <li><a class="hover:text-white transition-colors">이용약관</a></li>
            <li>
              <a class="text-indigo-400 font-medium hover:text-indigo-300 transition-colors">
                개인정보처리방침
              </a>
            </li>
            <li><a class="hover:text-white transition-colors">청소년 보호정책</a></li>
            <li><a class="hover:text-white transition-colors">위치기반서비스 이용약관</a></li>
          </ul>
        </div>

      </div>

      <!-- 하단 -->
      <div
        class="mt-5 pt-3 border-t border-white/10
               flex flex-col md:flex-row justify-between items-start md:items-center gap-2
               text-[11px] text-neutral-500"
      >
        <!-- 회사 정보 왼쪽 -->
        <p class="text-left md:text-left">© 2026 NEOMATH EDUTECH Inc.</p>

        <!-- 정책 링크 오른쪽 -->
        <div class="flex gap-4 mt-2 md:mt-0 justify-start md:justify-end w-full md:w-auto">
          <a class="hover:text-white transition-colors">이용약관</a>
          <a class="text-indigo-400 hover:text-indigo-300 transition-colors">개인정보처리방침</a>
        </div>
      </div>

    </div>
  </footer>
</template>
