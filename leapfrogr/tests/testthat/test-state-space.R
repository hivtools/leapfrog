test_that("can get state space info from C++", {
  ss_demog <- get_leapfrog_ss("DemographicProjection")

  expect_named(ss_demog)
  # SS variables might change, but test some here which are
  # unlikely to change.
  expect_equal(ss_demog$NS, 2)

  ss_child <- get_leapfrog_ss("ChildModel")

  expect_named(ss_child)
  expect_true(all(names(ss_demog) %in% names(ss_child)))
  expect_equal(dim(ss_child$hc2_to_ha_cd4_transition), c(7, 6))

  ss_coarse <- get_leapfrog_ss("HivCoarseAgeStratification")
  ss_full <- get_leapfrog_ss("HivFullAgeStratification")

  expect_named(ss_coarse)
  expect_named(ss_full)
  expect_true(ss_full$hAG > ss_coarse$hAG)
  expect_true(all(ss_full$hAG_span == 1))
})
