#include "gmock/gmock.h"

#include <string>

using namespace std;
using namespace testing;

TEST(ATest, IsTest) {
   ASSERT_TRUE( true );
}

TEST(ATest, IsATest) {
   ASSERT_FALSE( false );
}
