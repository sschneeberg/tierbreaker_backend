const request = require('supertest');
const assert = require('assert');

describe('Server', function () {
    describe('GET /ping', function () {
        it('should return a 200 status', function (done) {
            request('http://localhost:8000').get('/').expect(200, done);
        });
        it('should return pong', function (done) {
            request('http://localhost:8000')
                .get('/')
                .expect('Content-Type', /json/)
                .then((response) => {
                    assert(response.body.ping === 'pong', true);
                    done();
                })
                .catch((err) => done(err));
        });
    });
});

describe('Bracket Routes', function () {
    describe('GET /brackets', function () {
        it('should return a 200 status', function (done) {
            request('http://localhost:8000').get('/brackets').expect(200, done);
        });
        it('should return all brackets that are public', function (done) {
            request('http://localhost:8000')
                .get('/brackets')
                .expect('Content-Type', /json/)
                .then((response) => {
                    brackets = response.body.public_brackets;
                    for (let i = 0; i < brackets.length; i++) {
                        assert(brackets[i].private === false, true);
                    }
                    done();
                })
                .catch((err) => done(err));
        });
    });

    describe('GET /brackets/<bracket_key>', function () {
        it('should grab a single bracket for the given key', function (done) {
            key = '57000d62';
            request('http://localhost:8000')
                .get(`/bracket/${key}`)
                .expect(200)
                .expect('Content-Type', /json/)
                .then((response) => {
                    bracket = response.body;
                    assert(bracket.key === key, true);
                    done();
                })
                .catch((err) => done(err));
        });
    });

    // describe('POST /bracket/create', function () {
    //     it('should return build a bracket', function (done) {
    //         const opts = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight'];
    //         request('http://localhost:8000')
    //             .post('/bracket/create')
    //             .send({
    //                 options_list: opts,
    //                 duration: '4',
    //                 title: 'Who would win TWO',
    //                 num_options: '8',
    //                 private: true,
    //                 end_display: 'Winner'
    //             })
    //             .expect(200)
    //             .expect('Content-Type', /json/)
    //             .then((response) => {
    //                 bracket = response.body.bracket;
    //                 assert(bracket.num_rounds === Math.log2(8), true);
    //                 assert(bracket.time_duration === 4, true);
    //                 assert(bracket.round_duration === parseInt(4 / Math.log2(8)), true);
    //                 assert(bracket.title === 'Who would win TWO', true);
    //                 assert(bracket.end_display_format === 'Winner', true);
    //                 assert(bracket.private === true, true);
    //                 for (let i = 0; i < bracket.voting_options.round_options.length; i++) {
    //                     assert(bracket.voting_options.round_options[i] === opts[i], true);
    //                     assert(bracket.voting_options.totals[opts[i]] === 0, true);
    //                     assert(bracket.voting_options.votes[0][opts[i]] === 0, true);
    //                     assert(bracket.voting_options.votes.length === 1, true);
    //                 }
    //                 done();
    //             })
    //             .catch((err) => done(err));
    //     });
    // });
});
