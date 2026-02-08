<template>
  <!-- 상단 고정 네비게이션 바
       - 높이를 h-12로 고정해서 툴 느낌 유지
       - 배경은 완전 흰색
       - 하단 경계선만 살짝 줘서 영역 구분 -->
  <header
    class="
           h-12 flex items-center gap-2 px-3
           bg-white border-b border-zinc-200
           text-zinc-600 text-sm"
  >

    <!-- 좌측 로고 영역
         - 다른 요소들과 시각적으로 분리하기 위해 오른쪽에 border
         - 로고만 들어가므로 높이 작게 유지 -->
    <div class="flex items-center gap-2 pr-3 border-r border-zinc-200">
      <img src="/logo.png" class="h-5" />
    </div>

    <!-- 학원명 + 포인트 표시 영역
         - 글자 크기를 줄여서 네비가 튀지 않게 함
         - 포인트 숫자만 강조 -->
    <div class="flex items-center gap-1 text-xs">
      <!-- 유저 이름 -->
      <span class="font-semibold text-zinc-900">
        <!-- {{ auth.user.user_name }} -->
      </span>
      
      <!-- 유저 상태 -->
      <span class="font-semibold text-blue-600">
        <!-- {{ auth.user?.role === 'student' ? '학생회원' : '선생님' }} -->
      </span>

      <span class="text-zinc-400">|</span>
      <span class="text-zinc-500">
        <b class="text-zinc-900">8,750</b> P
      </span>
    </div>

    <!-- 메인 네비 버튼 영역
         - 실제 페이지 이동용 버튼들
         - ml-4로 좌측 정보 영역과 거리 확보 -->
    <nav class="flex items-center gap-1 ml-4">
      <NavBtn label="시험지" />
      <NavBtn label="학생관리" />
      <NavBtn label="문제DB" />
      <NavBtn label="서점" />
    </nav>

    <!-- 가운데 공간 확보용
         - 좌측 요소들과 우측 아이콘을 양 끝으로 밀어냄 -->
    <div class="flex-1" />

    <!-- 우측 아이콘 영역
         - 자주 누르는 기능만 배치
         - 버튼 크기 통일 -->
    <div class="flex items-center gap-1">
      <IconBtn icon="⟳" />
      <IconBtn icon="☰" />

      <!-- 사용자 프로필 버튼
           - 원형으로 처리해서 다른 아이콘과 구분 -->
      <button
        class="w-7 h-7 rounded-full
               flex items-center justify-center
               hover:bg-zinc-100 transition"
      >
        👤
      </button>
    </div>

  </header>
</template>

<script setup>
    import { useAuthStore } from '@/store/auth.js'

    const auth = useAuthStore()

    /*
    NavBtn
    - 상단 네비에 사용하는 텍스트 버튼 전용 컴포넌트
    - 높이와 패딩을 고정해서 버튼마다 크기 차이 없게 처리
    - 글자 수가 달라도 줄바꿈되지 않도록 whitespace-nowrap 사용
    */
    const NavBtn = {
    props: {
        label: String, // 버튼에 표시할 텍스트
    },
    template: `
        <button
        class="px-2 h-7 text-xs font-medium
                text-zinc-600 hover:text-zinc-900
                hover:bg-zinc-100 rounded transition whitespace-nowrap"
        >
        {{ label }}
        </button>
    `,
    }

    /*
    IconBtn
    - 아이콘 하나만 표시하는 버튼
    - 알림, 메뉴, 설정 같은 보조 기능용
    - 클릭 영역을 확보하면서도 네비 높이를 깨지 않게 설계
    */
    const IconBtn = {
    props: {
        icon: String, // 버튼 안에 표시할 아이콘 문자
    },
    template: `
        <button
        class="w-7 h-7 flex items-center justify-center
                text-zinc-500 hover:text-zinc-900
                hover:bg-zinc-100 rounded transition"
        >
        {{ icon }}
        </button>
    `,
    }
    auth
</script>
