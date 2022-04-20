# LostArk_Check_Quest
예전에 로아에서는 캐릭터가 주간 레이드, 일간 퀘스트, 일간 가디언토벌 등의 소위 말하는 휴식게이지가 정확하게 보이지 않아
제가 직접 한번 프로젝트를 통해 구상하여보기로 하여 프로젝트를 시작하였습니다.

2022-03-17
- Logo form은 항상 12시에 배치하도록 설계
- mainForm 구현 및 gui 제작
- 캐릭터명 입력 시 로아 정식 site에서 crawling data를 불러온 후 display하는 Load_data와 Character_load py생성
- 불러 온 캐릭터를 클릭 시 현재 에포나, 가디언 등을 입력하는 gui와 함수 구현

2022-03-18
- GUI 개선
- Cal_Days.py로 다음날과 다음주의 날짜 구하는 code 작성
- 휴식 게이지 날짜 지남에 따라 update하는 기능 구현 

문제점: 현재 날짜를 비교하여 업데이트 잘되지않음 추 후 개선 필요 

2022-03-21
 - 날짜 비교 업데이트 수정 완료 테스트 중 

2022-03-27
 - 날짜 비교 업데이트 수정 완료 테스트 중 

state_current = PINE & 0x0f; //sw번호 
		
		if(state_current == 0x00 && state_previous == 0x08)
		{
			_delay_ms(30);
			PORTD = 0x00;
			led_state = 0x00;
			_delay_ms(100);
		}
		
		else if(state_current == 0x00 && state_previous == 0x08)
		{
			_delay_ms(30);
			PORTD = 0x07;
			led_state = 0x07;
			_delay_ms(100);
		}
		
		state_previous = state_current;
	}*/
	
	//스위치를 활용한 led 점등
	while (1)
	{
		if((PINC&0x0F) == 0x0E)
		{
			PORTD = 0x02;
		}
		else if((PINC&0x0F) == 0x0D)
		{
			PORTD = 0x01;
		}
		else if((PINC&0x0F) == 0x07)
		{
			PORTD = 0x04;
		}
		else if((PINC&0x0F) == 0x0B)
		{
			PORTD = 0x00;
		}
	}
