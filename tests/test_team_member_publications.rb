# Run with: bundle exec ruby tests/test_team_member_publications.rb
require 'jekyll'
require 'tmpdir'
require 'fileutils'
require 'yaml'

root = File.expand_path('..', __dir__)

def assert_link_count(html, slug, expected)
  actual = html.scan(%(href="/publications/#{slug}/")).size
  raise "#{slug}: expected #{expected} link(s), got #{actual}" unless actual == expected
end

Dir.mktmpdir('team-publications-') do |source|
  %w[_layouts _team _publications _projects].each { |dir| FileUtils.mkdir_p(File.join(source, dir)) }
  FileUtils.cp(File.join(root, '_layouts/team_member.html'), File.join(source, '_layouts'))
  File.write(File.join(source, '_layouts/default.html'), '{{ content }}')
  File.write(File.join(source, '_layouts/publication.html'), '{{ content }}')
  FileUtils.cp(File.join(root, '_team/jannis-gries.md'), File.join(source, '_team'))
  File.write(File.join(source, '_team/jane-doe.md'), <<~PROFILE)
    ---
    layout: team_member
    name: "Prof. Dr. Jane Doe"
    ---
  PROFILE

  law_publications = %w[
    default-rules-as-a-means-of-european-integration
    codification-of-private-law-the-european-perspective
    uniform-law-legal-responses-to-globalisation
  ]
  law_publications.each do |slug|
    FileUtils.cp(File.join(root, "_publications/#{slug}.md"), File.join(source, '_publications'))
  end

  fixtures = {
    'author' => { 'authors' => ['Jane Doe'] },
    'proceedings' => { 'authors' => ['Jane Doe'], 'is_proceedings' => true },
    'editor' => { 'editors' => ['  jAnE dOe  '] },
    'contributor' => { 'contributors' => [{ 'name' => 'Jane Doe', 'role' => 'Review' }] },
    'multiple-roles' => {
      'authors' => [{ 'name' => 'Jane Doe' }],
      'editors' => [{ 'name' => 'Jane Doe' }],
      'contributors' => ['Jane Doe']
    },
    'hidden' => { 'editors' => ['Jane Doe'], 'published' => false },
    'unrelated' => { 'authors' => ['Janet Doe'], 'editors' => ['Jane Doe Smith'] },
    'book-editor-only' => { 'book_editors' => ['Jane Doe'] },
    'no-people' => {}
  }
  fixtures.each do |slug, fields|
    metadata = { 'title' => slug, 'year' => 2026 }.merge(fields)
    File.write(File.join(source, "_publications/#{slug}.md"), metadata.to_yaml + "---\n")
  end

  config = Jekyll.configuration(
    'source' => source,
    'destination' => File.join(source, '_site'),
    'quiet' => true,
    'collections' => {
      'team' => { 'output' => true, 'permalink' => '/team/:path/' },
      'publications' => { 'output' => true, 'permalink' => '/publications/:path/' },
      'projects' => { 'output' => false }
    }
  )
  Jekyll::Site.new(config).process

  jane_html = File.read(File.join(source, '_site/team/jane-doe/index.html'))
  %w[author proceedings editor contributor multiple-roles].each do |slug|
    assert_link_count(jane_html, slug, 1)
  end
  %w[hidden unrelated book-editor-only no-people].concat(law_publications).each do |slug|
    assert_link_count(jane_html, slug, 0)
  end

  jannis_html = File.read(File.join(source, '_site/team/jannis-gries/index.html'))
  law_publications.each { |slug| assert_link_count(jannis_html, slug, 1) }
  fixtures.each_key { |slug| assert_link_count(jannis_html, slug, 0) }
end

puts 'Publication profile links: all regression checks passed.'
